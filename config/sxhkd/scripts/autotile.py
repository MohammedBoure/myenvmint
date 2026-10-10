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

# Track window order per desktop to ensure stable layout
workspace_windows = {}
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

def retile_workspace(desktop_id):
    raw_windows = get_client_windows(desktop_id)
    raw_ids = [w['id'] for w in raw_windows]

    if desktop_id not in workspace_windows:
        workspace_windows[desktop_id] = []

    # Maintain stable ordering: keep existing, append new, drop closed
    current_order = [wid for wid in workspace_windows[desktop_id] if wid in raw_ids]
    for wid in raw_ids:
        if wid not in current_order:
            current_order.append(wid)
    workspace_windows[desktop_id] = current_order

    N = len(current_order)
    if N == 0:
        return

    wa_x, wa_y, wa_w, wa_h = get_workarea(desktop_id)
    usable_w = wa_w - 2 * OUTER_GAP
    usable_h = wa_h - 2 * OUTER_GAP

    if N == 1:
        # Fullscreen single tile with outer gap
        tile_window(current_order[0], wa_x + OUTER_GAP, wa_y + OUTER_GAP, usable_w, usable_h)
    elif N == 2:
        # 50-50 Binary Column Split with visible GAP and OUTER_GAP
        half_w = (usable_w - GAP) // 2
        tile_window(current_order[0], wa_x + OUTER_GAP, wa_y + OUTER_GAP, half_w, usable_h)
        x2 = wa_x + OUTER_GAP + half_w + GAP
        w2 = (wa_x + wa_w - OUTER_GAP) - x2
        tile_window(current_order[1], x2, wa_y + OUTER_GAP, w2, usable_h)
    elif N == 3:
        # Master-Stack: Left master (50%), Right stack of 2 (50% each vertically)
        master_w = (usable_w - GAP) // 2
        tile_window(current_order[0], wa_x + OUTER_GAP, wa_y + OUTER_GAP, master_w, usable_h)

        stack_x = wa_x + OUTER_GAP + master_w + GAP
        stack_w = (wa_x + wa_w - OUTER_GAP) - stack_x
        half_h = (usable_h - GAP) // 2

        tile_window(current_order[1], stack_x, wa_y + OUTER_GAP, stack_w, half_h)
        y3 = wa_y + OUTER_GAP + half_h + GAP
        h3 = (wa_y + wa_h - OUTER_GAP) - y3
        tile_window(current_order[2], stack_x, y3, stack_w, h3)
    elif N == 4:
        # 2x2 Grid
        half_w = (usable_w - GAP) // 2
        half_h = (usable_h - GAP) // 2
        col2_x = wa_x + OUTER_GAP + half_w + GAP
        col2_w = (wa_x + wa_w - OUTER_GAP) - col2_x
        row2_y = wa_y + OUTER_GAP + half_h + GAP
        row2_h = (wa_y + wa_h - OUTER_GAP) - row2_y

        tile_window(current_order[0], wa_x + OUTER_GAP, wa_y + OUTER_GAP, half_w, half_h)
        tile_window(current_order[1], wa_x + OUTER_GAP, row2_y, half_w, row2_h)
        tile_window(current_order[2], col2_x, wa_y + OUTER_GAP, col2_w, half_h)
        tile_window(current_order[3], col2_x, row2_y, col2_w, row2_h)
    else:
        # Generalized Master-Stack (Master on left, N-1 stacked vertically on right)
        master_w = (usable_w - GAP) // 2
        tile_window(current_order[0], wa_x + OUTER_GAP, wa_y + OUTER_GAP, master_w, usable_h)

        stack_x = wa_x + OUTER_GAP + master_w + GAP
        stack_w = (wa_x + wa_w - OUTER_GAP) - stack_x
        num_stack = N - 1
        total_stack_gaps = (num_stack - 1) * GAP
        each_h = (usable_h - total_stack_gaps) // num_stack

        for i in range(num_stack):
            cur_y = wa_y + OUTER_GAP + i * (each_h + GAP)
            if i == num_stack - 1:
                cur_h = (wa_y + wa_h - OUTER_GAP) - cur_y
            else:
                cur_h = each_h
            tile_window(current_order[1 + i], stack_x, cur_y, stack_w, cur_h)

    # Update 1px border colors
    update_borders(current_order)

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
