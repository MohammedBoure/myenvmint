# Sxhkd Configuration (`config/sxhkd/`)

This directory contains the Simple X Hotkey Daemon (sxhkd) configuration and its window management automation scripts.

## Files & Purposes

- **`sxhkdrc`**:
  The primary keyboard shortcut definition file. It configures:
  - Directional navigation (`Alt + h/j/k/l` or arrows).
  - Window management: non-destructive closing (`Alt + q`), fullscreen toggle (`Alt + f`), minimize (`Alt + m`), centering (`Alt + Shift + Space`), and fine resizing (`Alt + u/p/i/o`).
  - Workspaces 1 to 10 switching and window moving.
  - Quick application launching (`Alt + Ctrl + Enter` for terminal, `Alt + n` for xed, `Alt + Ctrl + t` for terminal at active directory).
- **`scripts/`**:
  Contains Python automation scripts used by sxhkd for GlazeWM-like window management.
