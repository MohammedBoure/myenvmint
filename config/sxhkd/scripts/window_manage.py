#!/usr/bin/env python3
import sys
import subprocess

def get_active_window():
    try:
        out = subprocess.check_output(['xdotool', 'getactivewindow'], stderr=subprocess.DEVNULL).decode().strip()
        wid = int(out)
        if wid > 0:
            return wid
    except Exception:
        pass
    try:
        out = subprocess.check_output(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stderr=subprocess.DEVNULL).decode()
        for token in out.split():
            if token.startswith('0x'):
                val = int(token.rstrip(','), 16)
                if val > 0:
                    return val
    except Exception:
        pass
    return None

def get_screen_size():
    try:
        out = subprocess.check_output(['xdotool', 'getdisplaygeometry'], stderr=subprocess.DEVNULL).decode().split()
        return int(out[0]), int(out[1])
    except Exception:
        return 1920, 1080

def get_win_geom(wid):
    out = subprocess.check_output(['xdotool', 'getwindowgeometry', '--shell', str(wid)], stderr=subprocess.DEVNULL).decode()
    geom = {}
    for line in out.strip().split('\n'):
        if '=' in line:
            k, v = line.split('=', 1)
            geom[k] = int(v)
    return geom.get('X', 0), geom.get('Y', 0), geom.get('WIDTH', 800), geom.get('HEIGHT', 600)

def resize_window(dim, delta_pct):
    wid = get_active_window()
    if not wid:
        return
    subprocess.run(['wmctrl', '-i', '-r', hex(wid), '-b', 'remove,fullscreen,maximized_vert,maximized_horz'], stderr=subprocess.DEVNULL)
    sw, sh = get_screen_size()
    x, y, w, h = get_win_geom(wid)
    
    if dim == 'width':
        delta = int(sw * delta_pct)
        if delta == 0:
            delta = 15 if delta_pct > 0 else -15
        new_w = max(100, min(sw, w + delta))
        subprocess.run(['xdotool', 'windowsize', str(wid), str(new_w), str(h)], stderr=subprocess.DEVNULL)
    elif dim == 'height':
        delta = int(sh * delta_pct)
        if delta == 0:
            delta = 15 if delta_pct > 0 else -15
        new_h = max(100, min(sh, h + delta))
        subprocess.run(['xdotool', 'windowsize', str(wid), str(w), str(new_h)], stderr=subprocess.DEVNULL)

def center_window():
    wid = get_active_window()
    if not wid:
        return
    subprocess.run(['wmctrl', '-i', '-r', hex(wid), '-b', 'remove,fullscreen,maximized_vert,maximized_horz'], stderr=subprocess.DEVNULL)
    sw, sh = get_screen_size()
    x, y, w, h = get_win_geom(wid)
    new_x = max(0, int((sw - w) / 2))
    new_y = max(0, int((sh - h) / 2))
    subprocess.run(['xdotool', 'windowmove', str(wid), str(new_x), str(new_y)], stderr=subprocess.DEVNULL)
    subprocess.run(['wmctrl', '-i', '-r', hex(wid), '-e', f'0,{new_x},{new_y},-1,-1'], stderr=subprocess.DEVNULL)

import time

def is_valid_client_window(wid):
    if not wid or wid <= 0:
        return False
    hex_id = hex(wid)
    try:
        wtype = subprocess.check_output(['xprop', '-id', hex_id, '_NET_WM_WINDOW_TYPE'], stderr=subprocess.DEVNULL).decode()
        if any(t in wtype for t in [
            '_NET_WM_WINDOW_TYPE_DESKTOP',
            '_NET_WM_WINDOW_TYPE_DOCK',
            '_NET_WM_WINDOW_TYPE_TOOLBAR',
            '_NET_WM_WINDOW_TYPE_MENU',
            '_NET_WM_WINDOW_TYPE_SPLASH'
        ]):
            return False
    except Exception:
        return False
    try:
        wstate = subprocess.check_output(['xprop', '-id', hex_id, '_NET_WM_STATE'], stderr=subprocess.DEVNULL).decode()
        if '_NET_WM_STATE_STICKY' in wstate:
            return False
    except Exception:
        pass
    return True

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

def get_target_window():
    # 1. Try currently active window
    try:
        out = subprocess.check_output(['xdotool', 'getactivewindow'], stderr=subprocess.DEVNULL).decode().strip()
        wid = int(out)
        if wid > 0 and is_valid_client_window(wid):
            return wid
    except Exception:
        pass

    # 2. Try _NET_ACTIVE_WINDOW on root
    try:
        out = subprocess.check_output(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stderr=subprocess.DEVNULL).decode()
        for token in out.split():
            if token.startswith('0x'):
                wid = int(token.rstrip(','), 16)
                if wid > 0 and is_valid_client_window(wid):
                    return wid
    except Exception:
        pass

    # 3. Try window under mouse pointer
    try:
        out = subprocess.check_output(['xdotool', 'getmouselocation', '--shell'], stderr=subprocess.DEVNULL).decode()
        for line in out.splitlines():
            if line.startswith('WINDOW='):
                wid = int(line.split('=')[1])
                if wid > 0 and is_valid_client_window(wid):
                    return wid
    except Exception:
        pass

    # 4. Fallback: Find topmost valid client on current desktop
    cur_desk = get_current_desktop()
    try:
        out = subprocess.check_output(['wmctrl', '-l'], stderr=subprocess.DEVNULL).decode()
        candidates = []
        for line in out.splitlines():
            parts = line.split(maxsplit=4)
            wid = int(parts[0], 16)
            desk = int(parts[1]) if parts[1].lstrip('-').isdigit() else -1
            if desk == cur_desk and is_valid_client_window(wid):
                candidates.append(wid)
        if candidates:
            return candidates[-1]
    except Exception:
        pass

    return None

def move_workspace(target_desk, follow=True):
    wid = get_target_window()
    if wid:
        # Move window to target workspace
        subprocess.run(['wmctrl', '-i', '-r', hex(wid), '-t', str(target_desk)], stderr=subprocess.DEVNULL)
        if follow:
            # Switch to target workspace so user moves with the window
            subprocess.run(['wmctrl', '-s', str(target_desk)], stderr=subprocess.DEVNULL)
            time.sleep(0.08)
            subprocess.run(['xdotool', 'windowactivate', str(wid)], stderr=subprocess.DEVNULL)
            subprocess.run(['wmctrl', '-i', '-a', hex(wid)], stderr=subprocess.DEVNULL)
    else:
        # If no window on current desktop, switch workspace directly
        switch_workspace(target_desk)

def switch_workspace(target_desk):
    subprocess.run(['wmctrl', '-s', str(target_desk)], stderr=subprocess.DEVNULL)
    time.sleep(0.08)
    # Focus topmost client window on destination workspace so user never has to click first
    try:
        out = subprocess.check_output(['wmctrl', '-l'], stderr=subprocess.DEVNULL).decode()
        for line in reversed(out.splitlines()):
            parts = line.split(maxsplit=4)
            wid = int(parts[0], 16)
            desk = int(parts[1]) if parts[1].lstrip('-').isdigit() else -1
            if desk == int(target_desk) and is_valid_client_window(wid):
                subprocess.run(['xdotool', 'windowactivate', str(wid)], stderr=subprocess.DEVNULL)
                subprocess.run(['wmctrl', '-i', '-a', hex(wid)], stderr=subprocess.DEVNULL)
                break
    except Exception:
        pass

def close_window():
    wid = get_target_window()
    if wid:
        subprocess.run(['wmctrl', '-i', '-c', hex(wid)], stderr=subprocess.DEVNULL)

if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) > 1 else ''
    if action == 'resize_w_dec':
        resize_window('width', -0.02)
    elif action == 'resize_w_inc':
        resize_window('width', 0.02)
    elif action == 'resize_h_dec':
        resize_window('height', -0.02)
    elif action == 'resize_h_inc':
        resize_window('height', 0.02)
    elif action == 'center':
        center_window()
    elif action == 'close':
        close_window()
    elif action == 'switch':
        desk = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        switch_workspace(desk)
    elif action == 'move':
        desk = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        move_workspace(desk, follow=True)
