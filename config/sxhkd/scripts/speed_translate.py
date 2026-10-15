#!/usr/bin/env python3
"""
Speed Translation Tool for MyEnvMint
Global shortcut: Win + Shift + X (Super + Shift + X)

Displays a quick text entry dialog (Zenity) where the user can type Arabic text.
Works seamlessly across all workspaces (never gets pinned to a foreign workspace).

Upon pressing Enter:
1. Normalizes the text (including translating '٩' to 'ج' according to environment rules).
2. Translates the text from Arabic (or auto-detected language) to English via Google Translate API.
3. Copies the translation to the system clipboard (xclip).
4. Restores focus to the target window on the CURRENT workspace and automatically pastes the translated English text (if triggered via dialog).
5. Displays a desktop notification confirming the translation and clipboard status.
"""

import os
import sys
import time
import json
import threading
import urllib.parse
import urllib.request
import subprocess

TERMINAL_CLASSES = (
    'xfce4-terminal', 'gnome-terminal', 'x-terminal-emulator', 'alacritty',
    'kitty', 'tilix', 'terminator', 'urxvt', 'xterm', 'rxvt', 'wezterm',
    'foot', 'qterminal', 'konsole', 'st', 'lxterminal'
)


def get_clean_env():
    """Return environment stripped of terminal-specific window tracking IDs."""
    env = os.environ.copy()
    env.pop('WINDOWID', None)
    env.pop('DESKTOP_STARTUP_ID', None)
    return env


def get_current_desktop():
    """Retrieve the current active workspace index (0-indexed)."""
    try:
        out = subprocess.check_output(
            ['xdotool', 'get_desktop'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return int(out)
    except Exception:
        pass
    try:
        out = subprocess.check_output(
            ['xprop', '-root', '_NET_CURRENT_DESKTOP'],
            stderr=subprocess.DEVNULL
        ).decode()
        for tok in out.split():
            if tok.isdigit():
                return int(tok)
    except Exception:
        pass
    return 0


def get_window_desktop(win_id):
    """Retrieve the workspace index of a given window."""
    if not win_id:
        return -1
    try:
        out = subprocess.check_output(
            ['xdotool', 'get_desktop_for_window', str(win_id)],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return int(out)
    except Exception:
        pass
    try:
        out = subprocess.check_output(
            ['xprop', '-id', str(win_id), '_NET_WM_DESKTOP'],
            stderr=subprocess.DEVNULL
        ).decode()
        for tok in out.split():
            if tok.isdigit():
                return int(tok)
    except Exception:
        pass
    return -1


def is_valid_client_window(win_id):
    """Check if the window is a valid application window (not desktop or panel)."""
    if not win_id:
        return False
    try:
        wm_class = subprocess.check_output(
            ['xprop', '-id', str(win_id), 'WM_CLASS'],
            stderr=subprocess.DEVNULL
        ).decode().lower()
        ignored = ['xfce4-panel', 'desktop', 'polybar', 'zenity']
        if any(ig in wm_class for ig in ignored):
            return False
        return True
    except Exception:
        return False


def get_target_window_on_current_desktop(cur_desk):
    """Find active or topmost client window strictly on the current workspace."""
    # 1. Check current active window
    try:
        act = subprocess.check_output(
            ['xdotool', 'getactivewindow'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        if act and get_window_desktop(act) == cur_desk and is_valid_client_window(act):
            return act
    except Exception:
        pass

    # 2. Check topmost client on cur_desk from wmctrl stack
    try:
        out = subprocess.check_output(['wmctrl', '-l'], stderr=subprocess.DEVNULL).decode()
        for line in reversed(out.splitlines()):
            parts = line.split(maxsplit=4)
            wid_str = parts[0]
            d = int(parts[1]) if parts[1].lstrip('-').isdigit() else -1
            wid_dec = str(int(wid_str, 16))
            if d == cur_desk and is_valid_client_window(wid_dec):
                return wid_dec
    except Exception:
        pass

    return None


def is_terminal_window(win_id):
    """Check if the specified window belongs to a terminal emulator."""
    if not win_id:
        return False
    try:
        out = subprocess.check_output(
            ['xprop', '-id', str(win_id), 'WM_CLASS'],
            stderr=subprocess.DEVNULL
        ).decode().lower()
        return any(term in out for term in TERMINAL_CLASSES)
    except Exception:
        return False


def pin_dialog_to_current_desktop(cur_desk):
    """Ensure the Zenity dialog is placed and focused on the current active workspace."""
    for _ in range(30):  # poll up to 1.5 seconds
        try:
            out = subprocess.check_output(['wmctrl', '-l'], stderr=subprocess.DEVNULL).decode()
            for line in out.splitlines():
                if 'Speed Translation' in line:
                    wid = line.split()[0]
                    # Assign strictly to current workspace
                    subprocess.run(['wmctrl', '-i', '-r', wid, '-t', str(cur_desk)], stderr=subprocess.DEVNULL)
                    # Keep on top
                    subprocess.run(['wmctrl', '-i', '-r', wid, '-b', 'add,above'], stderr=subprocess.DEVNULL)
                    # Activate and focus
                    subprocess.run(['wmctrl', '-i', '-a', wid], stderr=subprocess.DEVNULL)
                    subprocess.run(['xdotool', 'windowactivate', wid], stderr=subprocess.DEVNULL)
                    return
        except Exception:
            pass
        time.sleep(0.05)


def prompt_entry_dialog(cur_desk):
    """Display the Zenity input dialog for fast text entry on the current workspace."""
    # Launch watcher thread to immediately bind dialog to current workspace
    watcher = threading.Thread(target=pin_dialog_to_current_desktop, args=(cur_desk,), daemon=True)
    watcher.start()

    try:
        cmd = [
            'zenity',
            '--entry',
            '--title=Speed Translation (Arabic → English)',
            '--text=Enter text to translate (Arabic → English):',
            '--width=480',
            '--ok-label=Translate & Paste',
            '--cancel-label=Cancel'
        ]
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            env=get_clean_env()
        )
        if proc.returncode == 0:
            return proc.stdout.strip()
        return None
    except Exception:
        return None


def copy_to_clipboard(text):
    """Copy text to X11 clipboard selection for Ctrl+V / Ctrl+Shift+V paste."""
    try:
        proc = subprocess.Popen(
            ['xclip', '-selection', 'clipboard'],
            stdin=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=get_clean_env()
        )
        proc.communicate(input=text.encode('utf-8'))
    except Exception:
        pass


def translate_text(text, source_lang='auto', target_lang='en'):
    """Translate text using the Google Translate single API endpoint."""
    # Global environment normalization rule:
    # Character Mapping: '٩' (U+0669) -> 'ج' (U+062C)
    normalized_text = text.replace('\u0669', 'ج')

    encoded_text = urllib.parse.quote(normalized_text)
    url = (
        f'https://translate.googleapis.com/translate_a/single'
        f'?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={encoded_text}'
    )
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0'}
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        parts = [part[0] for part in data[0] if part and part[0]]
        return normalized_text, ''.join(parts).strip()


def send_notification(title, message, is_error=False):
    """Display a desktop notification."""
    try:
        icon = 'dialog-error' if is_error else 'accessories-character-map'
        subprocess.run([
            'notify-send',
            '-i', icon,
            '-t', '3500',
            title,
            message
        ], stderr=subprocess.DEVNULL, env=get_clean_env())
    except Exception:
        pass


def paste_to_window(win_id, is_term):
    """Refocus target window on current workspace and simulate paste shortcut."""
    if not win_id:
        return
    try:
        time.sleep(0.12)
        subprocess.run(['xdotool', 'windowactivate', '--sync', str(win_id)], stderr=subprocess.DEVNULL)
        time.sleep(0.08)

        # In terminals, Ctrl+Shift+V pastes from clipboard; in GUI apps, Ctrl+V
        if is_term:
            subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+shift+v'], stderr=subprocess.DEVNULL)
        else:
            subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+v'], stderr=subprocess.DEVNULL)
    except Exception:
        pass


def main():
    # 1. Resolve current active workspace and target window strictly on this workspace
    cur_desk = get_current_desktop()
    target_win = get_target_window_on_current_desktop(cur_desk)
    is_term = is_terminal_window(target_win) if target_win else False
    is_dialog_mode = False

    # 2. Get input text (either CLI argument or Zenity dialog on current workspace)
    if len(sys.argv) > 1:
        raw_input = ' '.join(sys.argv[1:]).strip()
    else:
        is_dialog_mode = True
        raw_input = prompt_entry_dialog(cur_desk)

    if not raw_input:
        sys.exit(0)

    # 3. Translate
    try:
        normalized_input, translated = translate_text(raw_input)
    except Exception as exc:
        copy_to_clipboard(raw_input)
        send_notification('Speed Translation Error', f'Failed to translate: {exc}\nOriginal text copied to clipboard.', is_error=True)
        sys.exit(1)

    if not translated:
        sys.exit(0)

    # 4. Copy to clipboard
    copy_to_clipboard(translated)

    # 5. If triggered via dialog, auto-paste into target window on this workspace
    if is_dialog_mode:
        paste_to_window(target_win, is_term)
    else:
        print(translated)

    # 6. Show desktop notification
    send_notification(
        'Speed Translation (Copied to Clipboard)',
        f'AR: {normalized_input}\nEN: {translated}'
    )


if __name__ == '__main__':
    main()
