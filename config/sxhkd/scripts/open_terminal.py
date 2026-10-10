#!/usr/bin/env python3
"""
Open Terminal Script for MyEnvMint
Opens a new terminal emulator instance at the current or last visited directory in any file manager
(Thunar, Nemo, Nautilus, Caja, PCManFM), or the active terminal's current working directory.
"""
import os
import sys
import subprocess
import time
from urllib.parse import unquote

CACHE_FILE = '/tmp/myenvmint_last_dir.txt'

FILE_MANAGER_CLASSES = ('thunar', 'nemo', 'nautilus', 'caja', 'pcmanfm', 'dolphin')
TERMINAL_CLASSES = (
    'xfce4-terminal', 'gnome-terminal', 'x-terminal-emulator', 'alacritty',
    'kitty', 'tilix', 'terminator', 'urxvt', 'xterm', 'rxvt', 'wezterm',
    'foot', 'qterminal', 'konsole', 'st', 'lxterminal'
)

def save_last_dir(path):
    try:
        if path and os.path.isdir(path):
            with open(CACHE_FILE, 'w') as f:
                f.write(path)
    except Exception:
        pass

def get_last_cached_dir():
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                p = f.read().strip()
                if p and os.path.isdir(p):
                    return p
    except Exception:
        pass
    return None

def get_active_window_info():
    try:
        active_id = subprocess.check_output(['xdotool', 'getactivewindow'], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return None, None, '', ''
    try:
        pid = subprocess.check_output(['xdotool', 'getwindowpid', active_id], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        pid = None
    try:
        wm_class = subprocess.check_output(['xprop', '-id', active_id, 'WM_CLASS'], stderr=subprocess.DEVNULL).decode().lower()
    except Exception:
        wm_class = ''
    try:
        title = subprocess.check_output(['xdotool', 'getwindowname', active_id], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        title = ''
    return active_id, pid, wm_class, title

def extract_from_file_manager_window(wid):
    """Safely extracts current directory path from any GTK file manager window while preserving clipboard."""
    try:
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk, Gdk
        Gtk.init([])
        clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        old_text = clip.wait_for_text()

        orig_active = None
        orig_desktop = None
        try:
            orig_active = subprocess.check_output(['xdotool', 'getactivewindow'], stderr=subprocess.DEVNULL).decode().strip()
        except Exception:
            pass
        try:
            orig_desktop = subprocess.check_output(['xdotool', 'get_desktop'], stderr=subprocess.DEVNULL).decode().strip()
        except Exception:
            pass

        str_wid = str(wid)
        needs_switch = (orig_active != str_wid)

        if needs_switch:
            subprocess.run(['xdotool', 'windowactivate', '--sync', str_wid], stderr=subprocess.DEVNULL)
            time.sleep(0.08)

        # Trigger path entry (ctrl+l), select all (ctrl+a), copy (ctrl+c), restore entry (Escape)
        subprocess.run(['xdotool', 'key', 'ctrl+l'], stderr=subprocess.DEVNULL)
        time.sleep(0.05)
        subprocess.run(['xdotool', 'key', 'ctrl+a'], stderr=subprocess.DEVNULL)
        time.sleep(0.05)
        subprocess.run(['xdotool', 'key', 'ctrl+c'], stderr=subprocess.DEVNULL)
        time.sleep(0.05)
        subprocess.run(['xdotool', 'key', 'Escape'], stderr=subprocess.DEVNULL)
        time.sleep(0.04)

        if needs_switch:
            if orig_active:
                subprocess.run(['xdotool', 'windowactivate', '--sync', orig_active], stderr=subprocess.DEVNULL)
            if orig_desktop:
                subprocess.run(['xdotool', 'set_desktop', orig_desktop], stderr=subprocess.DEVNULL)

        text = clip.wait_for_text()
        if old_text is not None:
            clip.set_text(old_text, -1)
            clip.store()

        if text:
            text = text.strip()
            if text.startswith('file://'):
                text = unquote(text[7:])
            if os.path.isdir(text):
                save_last_dir(text)
                return text
    except Exception:
        pass
    return None

def extract_from_terminal_pid(pid):
    """Finds the deepest active child shell/command cwd of a terminal process."""
    if not pid or not str(pid).isdigit():
        return None
    try:
        queue = [str(pid)]
        all_procs = []
        while queue:
            curr = queue.pop(0)
            all_procs.append(curr)
            try:
                ch = subprocess.check_output(['pgrep', '-P', curr], stderr=subprocess.DEVNULL).decode().split()
                queue.extend(ch)
            except Exception:
                pass

        for p in reversed(all_procs):
            cwd_link = f'/proc/{p}/cwd'
            if os.path.exists(cwd_link):
                try:
                    target = os.path.realpath(cwd_link)
                    if os.path.isdir(target):
                        save_last_dir(target)
                        return target
                except Exception:
                    pass
    except Exception:
        pass
    return None

def find_open_file_managers():
    """Finds all open file manager window IDs, prioritizing windows on the current desktop and stacking order."""
    fm_windows = []
    try:
        curr_desk = 0
        try:
            curr_desk = int(subprocess.check_output(['xdotool', 'get_desktop'], stderr=subprocess.DEVNULL).decode().strip())
        except Exception:
            pass

        stacking_wids = []
        try:
            xprop_out = subprocess.check_output(['xprop', '-root', '_NET_CLIENT_LIST_STACKING'], stderr=subprocess.DEVNULL).decode()
            if '#' in xprop_out:
                raw_ids = xprop_out.split('#', 1)[1].split(',')
                stacking_wids = [int(w.strip(), 16) for w in raw_ids if w.strip().startswith('0x')]
        except Exception:
            pass

        out = subprocess.check_output(['wmctrl', '-lx'], stderr=subprocess.DEVNULL).decode()
        for line in out.strip().splitlines():
            parts = line.split(None, 4)
            if len(parts) >= 3:
                wid_hex, desk_str, wm_class = parts[0], parts[1], parts[2].lower()
                title = parts[4] if len(parts) >= 5 else ''
                # Ignore desktop window (e.g. xfdesktop, nemo desktop)
                if 'desktop' in title.lower() and ('desktop' in wm_class):
                    continue
                if any(fmc in wm_class for fmc in FILE_MANAGER_CLASSES):
                    try:
                        desk_id = int(desk_str)
                    except ValueError:
                        desk_id = -1
                    wid_int = int(wid_hex, 16)
                    desk_score = 0 if desk_id == curr_desk else 1
                    stack_score = -(stacking_wids.index(wid_int) if wid_int in stacking_wids else -1)
                    fm_windows.append((desk_score, stack_score, wid_int))

        fm_windows.sort(key=lambda x: (x[0], x[1]))
        return [wid for _, _, wid in fm_windows]
    except Exception:
        return []

def get_target_directory():
    active_id, pid, wm_class, title = get_active_window_info()

    # 1. If currently active window is a file manager (Thunar, Nemo, Nautilus, Caja, PCManFM)
    if active_id and any(fmc in wm_class for fmc in FILE_MANAGER_CLASSES):
        target = extract_from_file_manager_window(active_id)
        if target:
            return target

    # 2. If currently active window is a terminal emulator
    if active_id and any(tc in wm_class for tc in TERMINAL_CLASSES):
        target = extract_from_terminal_pid(pid)
        if target:
            return target

    # 3. Check open file managers (current workspace prioritized, then stacking order)
    for fm_wid in find_open_file_managers():
        target = extract_from_file_manager_window(fm_wid)
        if target:
            return target

    # 4. Check cached directory from previous file manager or terminal visit
    cached = get_last_cached_dir()
    if cached:
        return cached

    # 5. Fallback to user home directory
    return os.path.expanduser('~')

def launch_terminal(target_dir):
    if not target_dir or not os.path.isdir(target_dir):
        target_dir = os.path.expanduser('~')

    os.chdir(target_dir)

    # Directly execute terminal emulator binaries with explicit working-directory option
    # (Avoids /usr/bin/x-terminal-emulator wrapper which discards --working-directory on Debian/Mint)
    if subprocess.run(['which', 'xfce4-terminal'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        subprocess.Popen(['xfce4-terminal', f'--working-directory={target_dir}'])
        return

    if subprocess.run(['which', 'gnome-terminal'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        subprocess.Popen(['gnome-terminal', f'--working-directory={target_dir}'])
        return

    if subprocess.run(['which', 'alacritty'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        subprocess.Popen(['alacritty', '--working-directory', target_dir])
        return

    if subprocess.run(['which', 'kitty'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        subprocess.Popen(['kitty', '--directory', target_dir])
        return

    subprocess.Popen(['x-terminal-emulator', f'--working-directory={target_dir}'])

def main():
    target_dir = get_target_directory()
    launch_terminal(target_dir)

if __name__ == '__main__':
    main()
