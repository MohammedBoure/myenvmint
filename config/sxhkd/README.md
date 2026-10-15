# Sxhkd Configuration (`config/sxhkd/`)

This directory contains the Simple X Hotkey Daemon (sxhkd) configuration and its window management automation scripts.

## Files & Purposes

- **`sxhkdrc`**:
  The primary keyboard shortcut definition file. It configures:
  - Directional navigation (`Alt + h/j/k/l` or arrows).
  - Window management: non-destructive closing (`Alt + q`), fullscreen toggle (`Alt + f`), minimize (`Alt + m`), centering (`Alt + Shift + Space`), and fine resizing (`Alt + u/p/i/o`).
  - Workspaces 1 to 10 switching (`Alt + 1..0`) with automatic client focus, and moving windows to workspaces (`Alt + Shift + 1..0`) with automatic viewport switching and smart window selection (no manual clicking required).
  - Quick application launching (`Alt + Ctrl + Enter` or `Alt + Ctrl + t` for terminal inheriting current/last file manager directory, `Alt + n` for xed).
  - Snipping Tool screenshot shortcut (`Win + Shift + S` / `Super + Shift + S`) to interactively select a screen region and copy it directly to the clipboard with desktop notification.
  - Speed Translation shortcut (`Win + Shift + X` / `Super + Shift + X`) with bilingual layout support: invokes an ultra-fast compiled C socket trigger to present a pre-warmed GTK3 floating bar instantly (< 2ms), translates Arabic to English over persistent keep-alive HTTPS, copies to clipboard in memory, automatically pastes at the cursor, and notifies.
- **`scripts/`**:
  Contains Python automation scripts used by sxhkd for GlazeWM-like binary tree window tiling, directional focus, workspace routing, context-aware terminal launching, and speed translation.
