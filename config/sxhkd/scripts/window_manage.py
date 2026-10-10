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

def close_window():
    wid = get_active_window()
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
