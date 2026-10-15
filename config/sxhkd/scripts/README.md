# Window Management Scripts (`config/sxhkd/scripts/`)

This directory contains the Python automation scripts that power the GlazeWM-style tiling and window navigation logic.

## Files & Purposes

- **`autotile.py`**:
  A lightweight event-driven daemon that monitors X11 window events via Xlib. It uses a dynamic Binary Tiling Tree (BSP) to automatically split the space of the currently focused window based on user position and aspect ratio, maintaining clean gaps and automatic layout restoration when windows are closed.

- **`focus.py`**:
  Calculates geometric distance vectors across all visible windows on the current monitor to switch focus directionally (`left`, `right`, `up`, `down`) relative to the currently active window.

- **`window_manage.py`**:
  Performs safe window and workspace operations including:
  - Non-destructive window close (`close`): sends an ICCCM `WM_DELETE_WINDOW` client message rather than killing the process (`SIGKILL`).
  - Centering (`center`): centers floating windows in the middle of the work area.
  - Resizing (`resize-width`, `resize-height`): increases or decreases window dimensions in fine 2% increments.
  - Workspace switching (`switch <N>`): switches to workspace N and automatically focuses its top client window.
  - Workspace moving (`move <N>`): resolves the target window (active window, window under pointer, or top client fallback), moves it to workspace N, switches view to workspace N, and focuses the moved window.

- **`open_terminal.py`**:
  Resolves the current or last visited directory in any active or open file manager (Thunar, Nemo, Nautilus, Caja, PCManFM) or active terminal session (via deep process cwd inspection, workspace and stacking prioritization, clipboard preservation, and persistent caching), launching the terminal directly into that directory.

- **`speed_translate.py`**:
  High-speed translation engine and dialog orchestrator. Pops up an interactive Zenity text entry window to input Arabic text, automatically normalizes typo characters (such as Arabic digit '٩' to 'ج'), translates the text to English using Google Translate's API, copies the result directly to the system clipboard (`xclip`), dynamically binds to and surfaces on whichever workspace is currently active (clearing inherited window IDs), restores focus to the target window on the current workspace, automatically pastes the translated English text, and issues a desktop notification.
