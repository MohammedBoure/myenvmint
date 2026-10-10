# Window Management Scripts (`config/sxhkd/scripts/`)

This directory contains the Python automation scripts that power the GlazeWM-style tiling and window navigation logic.

## Files & Purposes

- **`autotile.py`**:
  A lightweight event-driven daemon that monitors X11 window creation, mapping, and destruction via Xlib. It automatically arranges active client windows into clean tiled splits with configurable gaps and ignores dialogs, panels, and docks.

- **`focus.py`**:
  Calculates geometric distance vectors across all visible windows on the current monitor to switch focus directionally (`left`, `right`, `up`, `down`) relative to the currently active window.

- **`window_manage.py`**:
  Performs safe window operations including:
  - Non-destructive window close (`close`): sends an ICCCM `WM_DELETE_WINDOW` client message rather than killing the process (`SIGKILL`).
  - Centering (`center`): centers floating windows in the middle of the work area.
  - Resizing (`resize-width`, `resize-height`): increases or decreases window dimensions in fine 2% increments.

- **`open_terminal.py`**:
  Inspects the active window. If it is a Nemo file manager window, it resolves the current directory and spawns a new terminal directly inside that folder; otherwise, it opens the terminal in the user's home directory.
