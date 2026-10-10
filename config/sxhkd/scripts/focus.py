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

def get_windows(curr_desktop):
    windows = []
    try:
        out = subprocess.check_output(['wmctrl', '-lG'], stderr=subprocess.DEVNULL).decode()
        for line in out.strip().split('\n'):
            parts = line.split(None, 7)
            if len(parts) >= 8:
                wid_str, desk, x, y, w, h, host, title = parts
                wid = int(wid_str, 16)
                if int(desk) == curr_desktop:
                    if title in ['Desktop', 'xfce4-panel', 'cinnamon']:
                        continue
                    windows.append({
                        'id': wid,
                        'x': int(x),
                        'y': int(y),
                        'w': int(w),
                        'h': int(h),
                        'cx': int(x) + int(w) / 2.0,
                        'cy': int(y) + int(h) / 2.0,
                        'title': title
                    })
    except Exception:
        pass
    return windows

def focus_direction(direction):
    curr_desktop = get_current_desktop()
    windows = get_windows(curr_desktop)
    if not windows:
        return

    active_id = get_active_window()
    active_win = None
    if active_id:
        for w in windows:
            if w['id'] == active_id:
                active_win = w
                break

    if not active_win:
        target = windows[0]
        subprocess.run(['xdotool', 'windowactivate', str(target['id'])], stderr=subprocess.DEVNULL)
        subprocess.run(['wmctrl', '-i', '-a', f"0x{target['id']:08x}"], stderr=subprocess.DEVNULL)
        return

    if len(windows) == 1:
        return

    candidates = []
    acx = active_win['cx']
    acy = active_win['cy']

    for w in windows:
        if w['id'] == active_win['id']:
            continue
        cx = w['cx']
        cy = w['cy']
        dx = cx - acx
        dy = cy - acy

        if direction == 'left' and cx < acx:
            dist = -dx + 2.0 * abs(dy)
            candidates.append((dist, w))
        elif direction == 'right' and cx > acx:
            dist = dx + 2.0 * abs(dy)
            candidates.append((dist, w))
        elif direction == 'up' and cy < acy:
            dist = -dy + 2.0 * abs(dx)
            candidates.append((dist, w))
        elif direction == 'down' and cy > acy:
            dist = dy + 2.0 * abs(dx)
            candidates.append((dist, w))

    if candidates:
        candidates.sort(key=lambda item: item[0])
        target = candidates[0][1]
    else:
        # Fallback to window cycling
        sorted_wins = sorted(windows, key=lambda w: (w['x'], w['y']))
        idx = 0
        for i, w in enumerate(sorted_wins):
            if w['id'] == active_win['id']:
                idx = i
                break
        if direction in ['left', 'up']:
            target = sorted_wins[(idx - 1) % len(sorted_wins)]
        else:
            target = sorted_wins[(idx + 1) % len(sorted_wins)]

    subprocess.run(['xdotool', 'windowactivate', str(target['id'])], stderr=subprocess.DEVNULL)
    subprocess.run(['wmctrl', '-i', '-a', f"0x{target['id']:08x}"], stderr=subprocess.DEVNULL)

if __name__ == '__main__':
    dir_arg = sys.argv[1].lower() if len(sys.argv) > 1 else 'right'
    focus_direction(dir_arg)
