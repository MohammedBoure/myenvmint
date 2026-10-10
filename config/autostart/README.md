# Autostart Entries (`config/autostart/`)

This directory contains `.desktop` files deployed to `~/.config/autostart/` to launch environment services automatically upon user login.

## Files & Purposes

- **`myenvmint-init.desktop`**:
  Executes the master desktop environment startup orchestrator `~/.config/myenvmint/init-desktop.sh`. It cleanly coordinates display detection, workspace allocation, keyboard layouts, xmodmap keycode corrections, and sequentially spawns background daemons (`xcape`, `sxhkd`, `picom`, `polybar`, and `autotile.py`) while preventing duplicate instances.

- **`com.bitwarden.desktop.desktop`**:
  Launches the Bitwarden password manager upon desktop startup.
