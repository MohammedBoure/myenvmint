#!/usr/bin/env python3
"""
Dynamic Autotiling Daemon for Cinnamon / X11
Replicates GlazeWM tiling behavior (binary splits, master-stack, 2x2 grid)
Preserves native desktop panels, start menu, and Nemo file manager.
"""

import os
import sys
import time
import select
import subprocess
import Xlib.display
import Xlib.X
import Xlib.error

# Tiling configuration
GAP = 6
OUTER_GAP = 6
FLOATING_FILE = "/tmp/autotile_floating.txt"

# Track window order, trees, and active targets per desktop
workspace_windows = {}
workspace_trees = {}
last_active_windows = {}
_disp = None

def get_disp():
    global _disp
    if _disp is None:
        try:
            _disp = Xlib.display.Display()
            _disp.set_error_handler(lambda err, req: None)
        except Exception:
            pass
    return _disp

def get_floating_set():
    if not os.path.exists(FLOATING_FILE):
        return set()
    try:
        with open(FLOATING_FILE, "r") as f:
            return set(int(line.strip()) for line in f if line.strip().isdigit())
    except Exception:
        return set()

def get_current_desktop():
    try:
        out = subprocess.check_output(['wmctrl', '-d'], stderr=subprocess.DEVNULL).decode()
        for line in out.splitlines():
            if '*' in line:
                return int(line.split()[0])
    except Exception:
        pass
    try:
        out = subprocess.check_output(['xdotool', 'get_desktop'], stderr=subprocess.DEVNULL).decode().strip()
        return int(out)
    except Exception:
        return 0

def get_workarea(desktop_id):
    polybar_offset = 0
    try:
        res = subprocess.run(['pgrep', '-x', 'polybar'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode == 0:
            polybar_offset = 38
    except Exception:
        pass

    wa_x, wa_y, wa_w, wa_h = 0, 0, 1920, 1047
    try:
        out = subprocess.check_output(['xprop', '-root', '_NET_WORKAREA'], stderr=subprocess.DEVNULL).decode()
        if '=' in out:
            vals = [int(v.strip()) for v in out.split('=', 1)[1].split(',')]
            idx = desktop_id * 4
            if idx + 3 < len(vals):
                wa_x, wa_y, wa_w, wa_h = vals[idx], vals[idx+1], vals[idx+2], vals[idx+3]
    except Exception:
        try:
            out = subprocess.check_output(['xdotool', 'getdisplaygeometry'], stderr=subprocess.DEVNULL).decode().split()
            sw, sh = int(out[0]), int(out[1])
            wa_x, wa_y, wa_w, wa_h = 0, 0, sw, max(100, sh - 33)
        except Exception:
            wa_x, wa_y, wa_w, wa_h = 0, 0, 1920, 1047

    if polybar_offset > 0 and wa_y < polybar_offset:
        wa_h = max(100, wa_h - (polybar_offset - wa_y))
        wa_y = polybar_offset

    return wa_x, wa_y, wa_w, wa_h


def is_floating_or_ignored(wid):
    floating_set = get_floating_set()
    if wid in floating_set:
        return True

    hex_id = hex(wid)

    # 1. Check window state (minimized, modal, sticky, fullscreen, above)
    try:
        wm_state = subprocess.check_output(['xprop', '-id', hex_id, 'WM_STATE'], stderr=subprocess.DEVNULL).decode()
        if 'Iconic' in wm_state:
            return True
    except Exception:
        return True

    try:
        net_state = subprocess.check_output(['xprop', '-id', hex_id, '_NET_WM_STATE'], stderr=subprocess.DEVNULL).decode()
        if any(s in net_state for s in ['_NET_WM_STATE_MODAL', '_NET_WM_STATE_STICKY', '_NET_WM_STATE_FULLSCREEN', '_NET_WM_STATE_ABOVE']):
            return True
    except Exception:
        pass

    # 2. Check transient_for (dialogs / popups)
    try:
        trans = subprocess.check_output(['xprop', '-id', hex_id, 'WM_TRANSIENT_FOR'], stderr=subprocess.DEVNULL).decode()
        if 'window id #' in trans:
            return True
    except Exception:
        pass

    # 3. Check window type
    try:
        wtype = subprocess.check_output(['xprop', '-id', hex_id, '_NET_WM_WINDOW_TYPE'], stderr=subprocess.DEVNULL).decode()
        if any(t in wtype for t in [
            '_NET_WM_WINDOW_TYPE_DIALOG',
            '_NET_WM_WINDOW_TYPE_UTILITY',
            '_NET_WM_WINDOW_TYPE_TOOLBAR',
            '_NET_WM_WINDOW_TYPE_SPLASH',
            '_NET_WM_WINDOW_TYPE_DOCK',
            '_NET_WM_WINDOW_TYPE_DESKTOP',
            '_NET_WM_WINDOW_TYPE_NOTIFICATION',
            '_NET_WM_WINDOW_TYPE_MENU'
        ]):
            return True
    except Exception:
        pass

    # 4. Check class blacklist
    try:
        wm_class = subprocess.check_output(['xprop', '-id', hex_id, 'WM_CLASS'], stderr=subprocess.DEVNULL).decode().lower()
        floating_classes = [
            'zenity', 'yad', 'pavucontrol', 'nm-connection-editor',
            'cinnamon-settings', 'xfce4-settings', 'polkit',
            'gcr-prompter', 'display', 'wrapper-2.0', 'xfsettingsd'
        ]
        if any(fc in wm_class for fc in floating_classes):
            return True
    except Exception:
        pass

    # 5. Check title
    try:
        title = subprocess.check_output(['xdotool', 'getwindowname', str(wid)], stderr=subprocess.DEVNULL).decode().strip()
        if title in ['Desktop', 'xfce4-panel', 'cinnamon']:
            return True
    except Exception:
        pass

    return False

def get_client_windows(curr_desktop):
    windows = []
    try:
        out = subprocess.check_output(['wmctrl', '-lG'], stderr=subprocess.DEVNULL).decode()
        for line in out.strip().split('\n'):
            parts = line.split(None, 7)
            if len(parts) >= 8:
                wid_str, desk, x, y, w, h, host, title = parts
                wid = int(wid_str, 16)
                if int(desk) == curr_desktop:
                    if not is_floating_or_ignored(wid):
                        windows.append({
                            'id': wid,
                            'x': int(x),
                            'y': int(y),
                            'w': int(w),
                            'h': int(h),
                            'title': title
                        })
    except Exception:
        pass
    return windows

def strip_decorations(wid):
    disp = get_disp()
    if not disp:
        return
    try:
        motif_atom = disp.intern_atom('_MOTIF_WM_HINTS')
        win = disp.create_resource_object('window', wid)
        # MWM_HINTS_DECORATIONS = 2 (flags), decorations = 0
        win.change_property(motif_atom, motif_atom, 32, [2, 0, 0, 0, 0])
        disp.sync()
    except Exception:
        pass

def tile_window(wid, x, y, w, h):
    strip_decorations(wid)
    hex_id = hex(wid)
    subprocess.run(['wmctrl', '-i', '-r', hex_id, '-b', 'remove,maximized_vert,maximized_horz,fullscreen'], stderr=subprocess.DEVNULL)
    subprocess.run(['wmctrl', '-i', '-r', hex_id, '-e', f'0,{x},{y},{w},{h}'], stderr=subprocess.DEVNULL)

def get_active_window():
    try:
        out = subprocess.check_output(['xdotool', 'getactivewindow'], stderr=subprocess.DEVNULL).decode().strip()
        if out.isdigit():
            return int(out)
    except Exception:
        pass
    return None

def update_borders(current_order):
    if not current_order:
        return
    disp = get_disp()
    if not disp:
        return
    active_wid = get_active_window()
    white = 0xffffff
    gray = 0x3a3f4b
    root_id = disp.screen().root.id

    for wid in current_order:
        is_active = (wid == active_wid)
        color = white if is_active else gray
        try:
            win = disp.create_resource_object('window', wid)
            win.configure(border_width=1)
            win.change_attributes(border_pixel=color)
            parent = win.query_tree().parent
            if parent and parent.id != root_id:
                parent.configure(border_width=1)
                parent.change_attributes(border_pixel=color)
        except Exception:
            pass
    try:
        disp.sync()
    except Exception:
        pass

class TileNode:
    def __init__(self, wid=None, split='horizontal', ratio=0.5, left=None, right=None):
        self.wid = wid
        self.split = split  # 'horizontal' (side-by-side) or 'vertical' (stacked)
        self.ratio = ratio
        self.left = left
        self.right = right

    @property
    def is_leaf(self):
        return self.wid is not None

    def get_leaves(self):
        if self.is_leaf:
            return [self.wid]
        leaves = []
        if self.left:
            leaves.extend(self.left.get_leaves())
        if self.right:
            leaves.extend(self.right.get_leaves())
        return leaves

    def find_node(self, wid):
        if self.is_leaf:
            return self if self.wid == wid else None
        if self.left:
            found = self.left.find_node(wid)
            if found:
                return found
        if self.right:
            return self.right.find_node(wid)
        return None

    def remove_wid(self, wid):
        if self.is_leaf:
            return None if self.wid == wid else self
        if self.left:
            self.left = self.left.remove_wid(wid)
        if self.right:
            self.right = self.right.remove_wid(wid)
        if self.left is None:
            return self.right
        if self.right is None:
            return self.left
        return self

def compute_layout(node, x, y, w, h, gap, result):
    if node is None:
        return
    if node.is_leaf:
        result[node.wid] = (x, y, w, h)
        return
    if node.split == 'horizontal':
        w1 = max(50, int((w - gap) * node.ratio))
        w2 = max(50, (w - gap) - w1)
        x2 = x + w1 + gap
        compute_layout(node.left, x, y, w1, h, gap, result)
        compute_layout(node.right, x2, y, w2, h, gap, result)
    else:
        h1 = max(50, int((h - gap) * node.ratio))
        h2 = max(50, (h - gap) - h1)
        y2 = y + h1 + gap
        compute_layout(node.left, x, y, w, h1, gap, result)
        compute_layout(node.right, x, y2, w, h2, gap, result)

def insert_window(root, new_wid, target_wid, usable_w, usable_h, gap):
    if root is None:
        return TileNode(wid=new_wid)
    curr_layout = {}
    compute_layout(root, 0, 0, usable_w, usable_h, gap, curr_layout)
    target_node = None
    if target_wid and target_wid in curr_layout:
        target_node = root.find_node(target_wid)
    if not target_node:
        leaves = [wid for wid in curr_layout]
        if leaves:
            target_wid = leaves[-1]
            target_node = root.find_node(target_wid)
        else:
            return TileNode(wid=new_wid)

    tw_x, tw_y, tw_w, tw_h = curr_layout.get(target_wid, (0, 0, usable_w, usable_h))
    # If target window width >= height * 1.3, split horizontally; else split vertically
    split_dir = 'horizontal' if tw_w >= tw_h * 1.3 else 'vertical'

    old_wid = target_node.wid
    target_node.wid = None
    target_node.split = split_dir
    target_node.ratio = 0.5
    target_node.left = TileNode(wid=old_wid)
    target_node.right = TileNode(wid=new_wid)
    return root

def retile_workspace(desktop_id):
    raw_windows = get_client_windows(desktop_id)
    raw_ids = [w['id'] for w in raw_windows]

    wa_x, wa_y, wa_w, wa_h = get_workarea(desktop_id)
    usable_x = wa_x + OUTER_GAP
    usable_y = wa_y + OUTER_GAP
    usable_w = wa_w - 2 * OUTER_GAP
    usable_h = wa_h - 2 * OUTER_GAP

    root = workspace_trees.get(desktop_id)
    current_leaves = root.get_leaves() if root else []

    # 1. Remove closed / unmapped windows
    for wid in current_leaves:
        if wid not in raw_ids and root:
            root = root.remove_wid(wid)

    current_leaves = root.get_leaves() if root else []

    # 2. Determine target window where user was focused before event
    target_wid = last_active_windows.get(desktop_id)
    if target_wid not in current_leaves and current_leaves:
        target_wid = current_leaves[-1]

    # 3. Add any newly opened windows next to target window
    new_wids = [wid for wid in raw_ids if wid not in current_leaves]
    for wid in new_wids:
        root = insert_window(root, wid, target_wid, usable_w, usable_h, GAP)
        target_wid = wid

    workspace_trees[desktop_id] = root
    leaves = root.get_leaves() if root else []
    workspace_windows[desktop_id] = leaves

    # 4. Position and tile all windows in tree
    if root:
        layout = {}
        compute_layout(root, usable_x, usable_y, usable_w, usable_h, GAP, layout)
        for wid, (x, y, w, h) in layout.items():
            tile_window(wid, x, y, w, h)

    # 5. Update borders
    update_borders(leaves)

    # 6. Update last active window
    active_now = get_active_window()
    if active_now and not is_floating_or_ignored(active_now) and active_now in leaves:
        last_active_windows[desktop_id] = active_now

def run():
    disp = get_disp()
    root = disp.screen().root

    atom_client_list = disp.intern_atom('_NET_CLIENT_LIST')
    atom_current_desktop = disp.intern_atom('_NET_CURRENT_DESKTOP')
    atom_net_active = disp.intern_atom('_NET_ACTIVE_WINDOW')

    root.change_attributes(event_mask=Xlib.X.SubstructureNotifyMask | Xlib.X.PropertyChangeMask)

    # Initial tile on start
    curr_desk = get_current_desktop()
    retile_workspace(curr_desk)

    while True:
        try:
            # Wait up to 0.5s for events
            r, _, _ = select.select([disp.fileno()], [], [], 0.5)
            should_retile = False

            if r:
                while disp.pending_events() > 0:
                    event = disp.next_event()
                    if event.type in (Xlib.X.CreateNotify, Xlib.X.DestroyNotify, Xlib.X.MapNotify, Xlib.X.UnmapNotify):
                        should_retile = True
                    elif event.type == Xlib.X.PropertyNotify:
                        if event.atom in (atom_client_list, atom_current_desktop):
                            should_retile = True
                        elif event.atom == atom_net_active:
                            curr_desk = get_current_desktop()
                            active_now = get_active_window()
                            if active_now and not is_floating_or_ignored(active_now):
                                last_active_windows[curr_desk] = active_now
                            update_borders(workspace_windows.get(curr_desk, []))

            curr_desk = get_current_desktop()
            raw_wins = get_client_windows(curr_desk)
            raw_ids = [w['id'] for w in raw_wins]

            # Trigger retile on event or if window set changed
            if should_retile or (raw_ids != workspace_windows.get(curr_desk, [])):
                time.sleep(0.08)
                retile_workspace(curr_desk)

        except Xlib.error.XError:
            pass
        except Exception as e:
            time.sleep(0.1)

def daemonize():
    if os.fork() > 0:
        sys.exit(0)
    os.setsid()
    if os.fork() > 0:
        sys.exit(0)

    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    si = open(os.devnull, 'r')
    so = open('/tmp/autotile.log', 'a+')
    se = open('/tmp/autotile.log', 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

    with open('/tmp/autotile.pid', 'w') as f:
        f.write(str(os.getpid()))

if __name__ == '__main__':
    if '--foreground' not in sys.argv:
        daemonize()
    try:
        run()
    except KeyboardInterrupt:
        sys.exit(0)
