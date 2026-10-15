#!/usr/bin/env python3
"""
Speed Translation Tool for MyEnvMint
Global shortcut: Win + Shift + X (Super + Shift + X)

Displays a quick text entry dialog (Zenity) where the user can type Arabic text.
Upon pressing Enter:
1. Normalizes the text (including translating '٩' to 'ج' according to environment rules).
2. Translates the text from Arabic (or auto-detected language) to English via Google Translate API.
3. Copies the translation to both system clipboard and primary selection buffers (xclip).
4. Restores focus to the previously active window and automatically pastes the translated English text (if triggered via dialog).
5. Displays a desktop notification confirming the translation and clipboard status.
"""

import sys
import time
import json
import urllib.parse
import urllib.request
import subprocess

TERMINAL_CLASSES = (
    'xfce4-terminal', 'gnome-terminal', 'x-terminal-emulator', 'alacritty',
    'kitty', 'tilix', 'terminator', 'urxvt', 'xterm', 'rxvt', 'wezterm',
    'foot', 'qterminal', 'konsole', 'st', 'lxterminal'
)


def get_active_window():
    """Retrieve the currently focused window ID before the dialog is launched."""
    try:
        out = subprocess.check_output(
            ['xdotool', 'getactivewindow'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return out if out else None
    except Exception:
        return None


def is_terminal_window(win_id):
    """Check if the specified window belongs to a terminal emulator."""
    if not win_id:
        return False
    try:
        out = subprocess.check_output(
            ['xprop', '-id', win_id, 'WM_CLASS'],
            stderr=subprocess.DEVNULL
        ).decode().lower()
        return any(term in out for term in TERMINAL_CLASSES)
    except Exception:
        return False


def prompt_entry_dialog():
    """Display the Zenity input dialog for fast text entry."""
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
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
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
            stderr=subprocess.DEVNULL
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
        ], stderr=subprocess.DEVNULL)
    except Exception:
        pass


def paste_to_window(win_id, is_term):
    """Refocus target window and simulate paste shortcut."""
    if not win_id:
        return
    try:
        # Give a small pause for Zenity to completely unmap and WM to restore focus
        time.sleep(0.12)
        subprocess.run(['xdotool', 'windowactivate', '--sync', win_id], stderr=subprocess.DEVNULL)
        time.sleep(0.08)

        # In terminals, Ctrl+Shift+V pastes from clipboard; in GUI apps, Ctrl+V
        if is_term:
            subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+shift+v'], stderr=subprocess.DEVNULL)
        else:
            subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+v'], stderr=subprocess.DEVNULL)
    except Exception:
        pass


def main():
    # 1. Capture previously active window before any dialog appears
    prev_win = get_active_window()
    is_term = is_terminal_window(prev_win)
    is_dialog_mode = False

    # 2. Get input text (either CLI argument or Zenity dialog)
    if len(sys.argv) > 1:
        raw_input = ' '.join(sys.argv[1:]).strip()
    else:
        is_dialog_mode = True
        raw_input = prompt_entry_dialog()

    if not raw_input:
        sys.exit(0)

    # 3. Translate
    try:
        normalized_input, translated = translate_text(raw_input)
    except Exception as exc:
        # On translation failure, copy raw text to clipboard and notify
        copy_to_clipboard(raw_input)
        send_notification('Speed Translation Error', f'Failed to translate: {exc}\nOriginal text copied to clipboard.', is_error=True)
        sys.exit(1)

    if not translated:
        sys.exit(0)

    # 4. Copy to clipboard
    copy_to_clipboard(translated)

    # 5. If triggered via dialog, auto-paste into previous window
    if is_dialog_mode:
        paste_to_window(prev_win, is_term)
    else:
        print(translated)

    # 6. Show desktop notification
    send_notification(
        'Speed Translation (Copied to Clipboard)',
        f'AR: {normalized_input}\nEN: {translated}'
    )


if __name__ == '__main__':
    main()
