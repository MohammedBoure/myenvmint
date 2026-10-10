#!/usr/bin/env python3
"""
Open Terminal Script for MyEnvMint
Opens a new terminal emulator instance at the current or last visited directory in the file manager (Nemo/Thunar),
or the active terminal's current working directory.
"""
import os
import sys
import subprocess
import time

CACHE_FILE = '/tmp/myenvmint_last_dir.txt'

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

def extract_from_nemo_window(wid):
    """Safely extracts current directory path from a Nemo window while preserving existing clipboard."""
    try:
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk, Gdk
        Gtk.init([])
        clip = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        old_text = clip.wait_for_text()

        orig_active = None
        try:
            orig_active = subprocess.check_output(['xdotool', 'getactivewindow'], stderr=subprocess.DEVNULL).decode().strip()
        except Exception:
            pass

        subprocess.run(['xdotool', 'windowactivate', '--sync', str(wid)], stderr=subprocess.DEVNULL)
        time.sleep(0.04)
        subprocess.run(['xdotool', 'key', 'ctrl+l'], stderr=subprocess.DEVNULL)
        time.sleep(0.04)
        subprocess.run(['xdotool', 'key', 'ctrl+c'], stderr=subprocess.DEVNULL)
        time.sleep(0.04)
        subprocess.run(['xdotool', 'key', 'Escape'], stderr=subprocess.DEVNULL)
        time.sleep(0.02)

        if orig_active and orig_active != str(wid):
            subprocess.run(['xdotool', 'windowactivate', '--sync', orig_active], stderr=subprocess.DEVNULL)

        text = clip.wait_for_text()
        if old_text:
            clip.set_text(old_text, -1)
            clip.store()

        if text:
            text = text.strip()
            if text.startswith('file://'):
                text = text[7:]
            if os.path.isdir(text):
                save_last_dir(text)
                return text
    except Exception:
        pass
    return None

def get_target_directory():
    active_id, pid, wm_class, title = get_active_window_info()

    # 1. If currently active window is Nemo, extract directly
    if active_id and 'nemo' in wm_class:
        target = extract_from_nemo_window(active_id)
        if target:
            return target

    # 2. If active window is a terminal or has shell children, extract its cwd
    if pid and pid.isdigit():
        try:
            children = subprocess.check_output(['pgrep', '-P', pid], stderr=subprocess.DEVNULL).decode().split()
            for child in reversed(children):
                cwd_link = f'/proc/{child}/cwd'
                if os.path.exists(cwd_link):
                    target = os.path.realpath(cwd_link)
                    if os.path.isdir(target):
                        save_last_dir(target)
                        return target
            cwd_link = f'/proc/{pid}/cwd'
            if os.path.exists(cwd_link):
                target = os.path.realpath(cwd_link)
                if os.path.isdir(target):
                    save_last_dir(target)
                    return target
        except Exception:
            pass

    # 3. Check any currently open Nemo windows
    try:
        wids = subprocess.check_output(['xdotool', 'search', '--class', 'nemo'], stderr=subprocess.DEVNULL).decode().split()
        for wid in reversed(wids):
            name = subprocess.check_output(['xdotool', 'getwindowname', wid], stderr=subprocess.DEVNULL).decode().strip()
            if name and name != 'Desktop':
                target = extract_from_nemo_window(wid)
                if target:
                    return target
                break
    except Exception:
        pass

    # 4. Check last cached directory from previous Nemo/terminal visit
    cached = get_last_cached_dir()
    if cached:
        return cached

    # 5. Fallback to user home directory
    return os.path.expanduser('~')

def main():
    target_dir = get_target_directory()
    if not target_dir or not os.path.isdir(target_dir):
        target_dir = os.path.expanduser('~')

    os.chdir(target_dir)
    subprocess.Popen(['x-terminal-emulator', f'--working-directory={target_dir}'])

if __name__ == '__main__':
    main()
