#!/usr/bin/env python3
"""
Ultra-Fast Speed Translation Tool for MyEnvMint
Global shortcut: Win + Shift + X (Super + Shift + X)

Designed for MAXIMUM SPEED:
- Runs as a resident background daemon with a pre-warmed GTK3 floating bar.
- Pre-warmed persistent HTTPS connection to Google Translate API (eliminates TLS/DNS handshakes).
- Instantaneous trigger via UNIX domain socket datagram (< 1 millisecond).
- Universal workspace adherence (sticky across all desktops with zero positioning latency).
- Immediate window dismissal on Enter (0ms perceived delay) and background auto-paste.
- Character mapping: '٩' (U+0669) -> 'ج' (U+062C).
"""

import os
import sys
import time
import json
import socket
import threading
import http.client
import urllib.parse
import subprocess

SOCK_PATH = '/tmp/speed_translate.sock'
PID_PATH = '/tmp/speed_translate.pid'

TERMINAL_CLASSES = (
    'xfce4-terminal', 'gnome-terminal', 'x-terminal-emulator', 'alacritty',
    'kitty', 'tilix', 'terminator', 'urxvt', 'xterm', 'rxvt', 'wezterm',
    'foot', 'qterminal', 'konsole', 'st', 'lxterminal'
)


class PersistentTranslator:
    """Maintains a persistent HTTPS keep-alive connection to eliminate handshake latency."""
    def __init__(self):
        self.conn = None

    def get_connection(self):
        if self.conn is None:
            self.conn = http.client.HTTPSConnection('translate.googleapis.com', 443, timeout=5)
            self.conn.connect()
        return self.conn

    def translate(self, text, source='auto', target='en'):
        # Global environment normalization rule: '٩' -> 'ج'
        normalized = text.replace('\u0669', 'ج')
        encoded = urllib.parse.quote(normalized)
        path = f'/translate_a/single?client=gtx&sl={source}&tl={target}&dt=t&q={encoded}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Connection': 'keep-alive'
        }

        # Attempt with keep-alive; if connection dropped during idle, reconnect and retry once
        for attempt in range(2):
            try:
                conn = self.get_connection()
                conn.request('GET', path, headers=headers)
                resp = conn.getresponse()
                data = json.loads(resp.read().decode('utf-8'))
                parts = [part[0] for part in data[0] if part and part[0]]
                return normalized, ''.join(parts).strip()
            except Exception:
                if self.conn:
                    try:
                        self.conn.close()
                    except Exception:
                        pass
                self.conn = None
                if attempt == 1:
                    raise


class SpeedTranslateApp:
    def __init__(self):
        self.translator = PersistentTranslator()
        self.target_win = None
        self.is_terminal = False
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        # Setup GTK Window
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_title('Speed Translation')
        self.window.set_role('SpeedTranslation')
        self.window.set_decorated(False)
        self.window.set_default_size(540, 56)
        self.window.set_resizable(False)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.stick()
        self.window.set_keep_above(True)
        self.window.set_skip_taskbar_hint(True)
        self.window.set_skip_pager_hint(True)

        # Container
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.window.add(box)

        # Entry Widget
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text('Type Arabic text & press Enter (Esc to cancel)...')
        self.entry.connect('activate', self.on_activate)
        box.pack_start(self.entry, True, True, 0)

        # Window Signals
        self.window.connect('key-press-event', self.on_key_press)
        self.window.connect('focus-out-event', self.on_focus_out)

        # Modern CSS Dark Glass Theme
        css = b'''
        window {
            background-color: #1e1e2e;
            border: 2px solid #5294e2;
            border-radius: 12px;
        }
        entry {
            background: transparent;
            border: none;
            color: #ffffff;
            font-size: 16px;
            font-weight: 500;
            padding: 12px 18px;
            caret-color: #5294e2;
        }
        entry selection {
            background-color: #5294e2;
            color: #ffffff;
        }
        '''
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Setup Socket Listener for instant hotkey triggers
        self.setup_socket()

        # Pre-warm connection in background
        threading.Thread(target=self.warmup_connection, daemon=True).start()

    def warmup_connection(self):
        try:
            self.translator.get_connection()
        except Exception:
            pass

    def setup_socket(self):
        if os.path.exists(SOCK_PATH):
            try:
                os.remove(SOCK_PATH)
            except Exception:
                pass
        self.server_sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server_sock.bind(SOCK_PATH)
        self.server_sock.setblocking(False)
        GLib.io_add_watch(self.server_sock.fileno(), GLib.IO_IN, self.on_socket_trigger)

    def on_socket_trigger(self, source, condition):
        try:
            self.server_sock.recvfrom(1024)
        except Exception:
            return True

        # 1. Capture active window before presenting dialog
        self.target_win = self.get_active_window()
        self.is_terminal = self.is_terminal_window(self.target_win) if self.target_win else False

        # 2. Present window instantly
        self.entry.set_text('')
        self.window.stick()
        self.window.set_keep_above(True)
        self.window.show_all()
        self.window.present_with_time(Gdk.CURRENT_TIME)
        self.entry.grab_focus()
        return True

    def get_active_window(self):
        try:
            out = subprocess.check_output(
                ['xdotool', 'getactivewindow'],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            wid = int(out)
            # Ignore self window
            my_xid = self.window.get_window().get_xid() if self.window.get_window() else 0
            if wid and wid != my_xid:
                return wid
        except Exception:
            pass
        return None

    def is_terminal_window(self, win_id):
        if not win_id:
            return False
        try:
            wm_class = subprocess.check_output(
                ['xprop', '-id', str(win_id), 'WM_CLASS'],
                stderr=subprocess.DEVNULL
            ).decode().lower()
            return any(term in wm_class for term in TERMINAL_CLASSES)
        except Exception:
            return False

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.dismiss()
            return True
        return False

    def on_focus_out(self, widget, event):
        # Auto-dismiss when clicking elsewhere
        if self.window.get_visible():
            self.dismiss()
        return False

    def dismiss(self):
        self.window.hide()
        if self.target_win:
            try:
                subprocess.run(['xdotool', 'windowactivate', str(self.target_win)], stderr=subprocess.DEVNULL)
            except Exception:
                pass

    def on_activate(self, entry):
        raw_text = entry.get_text().strip()
        # Step 1: Instantly hide window (0ms perceived latency)
        self.window.hide()
        target = self.target_win
        is_term = self.is_terminal

        if not raw_text:
            return

        # Refocus target window immediately
        if target:
            try:
                subprocess.run(['xdotool', 'windowactivate', str(target)], stderr=subprocess.DEVNULL)
            except Exception:
                pass

        # Step 2: Background translation and instant paste
        threading.Thread(
            target=self.process_translation,
            args=(raw_text, target, is_term),
            daemon=True
        ).start()

    def process_translation(self, raw_text, target_win, is_term):
        try:
            normalized_input, translated = self.translator.translate(raw_text)
        except Exception as exc:
            self.copy_to_system_clipboard(raw_text)
            self.notify('Speed Translation Error', f'Translation failed: {exc}', is_error=True)
            return

        if not translated:
            return

        # Copy to GTK clipboard and xclip
        self.copy_to_system_clipboard(translated)

        # Instant auto-paste into target window
        if target_win:
            paste_key = 'ctrl+shift+v' if is_term else 'ctrl+v'
            try:
                subprocess.run([
                    'xdotool', 'key', '--window', str(target_win), '--clearmodifiers', paste_key
                ], stderr=subprocess.DEVNULL)
            except Exception:
                pass

        # Desktop notification
        self.notify(
            'Speed Translation',
            f'AR: {normalized_input}\nEN: {translated}'
        )

    def copy_to_system_clipboard(self, text):
        # 1. Native GTK in-memory clipboard
        GLib.idle_add(self._set_gtk_clipboard, text)
        # 2. X11 clipboard via xclip
        try:
            p = subprocess.Popen(
                ['xclip', '-selection', 'clipboard'],
                stdin=subprocess.PIPE,
                stderr=subprocess.DEVNULL
            )
            p.communicate(input=text.encode('utf-8'))
        except Exception:
            pass

    def _set_gtk_clipboard(self, text):
        self.clipboard.set_text(text, -1)
        self.clipboard.store()
        return False

    def notify(self, title, message, is_error=False):
        try:
            icon = 'dialog-error' if is_error else 'accessories-character-map'
            subprocess.run([
                'notify-send',
                '-i', icon,
                '-t', '3000',
                title,
                message
            ], stderr=subprocess.DEVNULL)
        except Exception:
            pass


def send_trigger():
    """Send datagram to resident daemon socket; returns True on success."""
    if not os.path.exists(SOCK_PATH):
        return False
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.sendto(b'1', SOCK_PATH)
        s.close()
        return True
    except Exception:
        return False


def daemonize():
    """Double-fork daemonization to completely detach from parent terminal."""
    if os.fork() > 0:
        sys.exit(0)
    os.setsid()
    if os.fork() > 0:
        sys.exit(0)
    sys.stdout.flush()
    sys.stderr.flush()
    si = open(os.devnull, 'r')
    so = open('/tmp/speed_translate.log', 'a+')
    se = open('/tmp/speed_translate.log', 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def main():
    # Remove terminal-specific window IDs from environment
    os.environ.pop('WINDOWID', None)
    os.environ.pop('DESKTOP_STARTUP_ID', None)

    # CLI direct translation mode: speed-translate "text"
    if len(sys.argv) > 1 and sys.argv[1] not in ('daemon', 'trigger'):
        raw_input = ' '.join(sys.argv[1:]).strip()
        translator = PersistentTranslator()
        try:
            normalized_input, translated = translator.translate(raw_input)
            print(translated)
            # Copy to clipboard
            p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            p.communicate(input=translated.encode('utf-8'))
        except Exception as exc:
            print(f'Error: {exc}', file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    # Trigger mode from hotkey:
    if len(sys.argv) > 1 and sys.argv[1] == 'trigger':
        if send_trigger():
            sys.exit(0)
        # If daemon wasn't running, start it
        subprocess.Popen(['python3', __file__, 'daemon'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.15)
        send_trigger()
        sys.exit(0)

    # Daemon mode: double-fork detach
    if len(sys.argv) > 1 and sys.argv[1] == 'daemon':
        if '--foreground' not in sys.argv:
            daemonize()
    elif len(sys.argv) == 1:
        # Check if daemon already running; if so, trigger it and exit
        if send_trigger():
            sys.exit(0)

    # Write PID
    with open(PID_PATH, 'w') as f:
        f.write(str(os.getpid()))

    global Gtk, Gdk, GLib
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib

    # Run resident application
    app = SpeedTranslateApp()
    # If launched without 'daemon' arg, trigger immediately on launch
    if len(sys.argv) == 1:
        GLib.idle_add(lambda: app.on_socket_trigger(None, None))

    Gtk.main()


if __name__ == '__main__':
    main()
