# Autostart Entries (`config/autostart/`)

This directory contains `.desktop` files deployed to `~/.config/autostart/` to launch environment services automatically upon user login.

## Files & Purposes

- **`myenvmint-init.desktop`**:
  Executes the master orchestrator `~/.config/myenvmint/init-desktop.sh` to ensure all workspaces, keyboard layouts, and background services are properly initialized.

- **`sxhkd.desktop`**:
  Launches the sxhkd shortcut daemon.

- **`polybar.desktop`**:
  Executes `~/.config/polybar/launch.sh` to initialize the top bar.

- **`picom.desktop`**:
  Spawns the Picom compositor in daemon mode.

- **`autotile.desktop`**:
  Runs the `autotile.py` window tiling daemon.

- **`xcape.desktop`**:
  Runs `xcape -e 'Super_L=Super_L|F1'` to bind a standalone tap of the Super key to the application menu without interfering with `Super + Space` or modifier shortcuts.

- **`com.bitwarden.desktop.desktop`**:
  Launches the Bitwarden password manager upon desktop startup.
