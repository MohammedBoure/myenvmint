#!/usr/bin/env python3
import os
import sys
import subprocess

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
        wm_class = subprocess.check_output(['xprop', '-id', active_id, 'WM_CLASS'], stderr=subprocess.DEVNULL).decode()
    except Exception:
        wm_class = ''
    try:
        title = subprocess.check_output(['xdotool', 'getwindowname', active_id], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        title = ''
    return active_id, pid, wm_class, title

def get_target_directory():
    active_id, pid, wm_class, title = get_active_window_info()
    if not active_id:
        return os.path.expanduser('~')

    if 'nemo' in wm_class.lower():
        try:
            import gi
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk, Gdk

            subprocess.run(['xdotool', 'key', '--window', active_id, 'ctrl+l'], stderr=subprocess.DEVNULL)
            subprocess.run(['xdotool', 'key', '--window', active_id, 'ctrl+c'], stderr=subprocess.DEVNULL)
            subprocess.run(['xdotool', 'key', '--window', active_id, 'Escape'], stderr=subprocess.DEVNULL)

            clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            text = clip.wait_for_text()
            if text:
                text = text.strip()
                if text.startswith('file://'):
                    text = text[7:]
                if os.path.isdir(text):
                    return text
        except Exception:
            pass

    if pid and pid.isdigit():
        try:
            children = subprocess.check_output(['pgrep', '-P', pid], stderr=subprocess.DEVNULL).decode().split()
            for child in reversed(children):
                cwd_link = f'/proc/{child}/cwd'
                if os.path.exists(cwd_link):
                    target = os.path.realpath(cwd_link)
                    if os.path.isdir(target):
                        return target
            cwd_link = f'/proc/{pid}/cwd'
            if os.path.exists(cwd_link):
                target = os.path.realpath(cwd_link)
                if os.path.isdir(target):
                    return target
        except Exception:
            pass

    return os.path.expanduser('~')

def main():
    target_dir = get_target_directory()
    if not os.path.isdir(target_dir):
        target_dir = os.path.expanduser('~')
    os.chdir(target_dir)
    subprocess.Popen(['x-terminal-emulator'])

if __name__ == '__main__':
    main()
