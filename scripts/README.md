# Scripts Directory (`scripts/`)

This directory contains the core management, deployment, and orchestration shell scripts for the MyEnvMint environment.

## Files & Purposes

- **`apply.sh`**:
  Synchronizes configuration files from this repository directly into the user's home configuration (`~/.config/`, `~/.zshrc`, `~/.gemini/`, etc.) and immediately reloads all active daemons (sxhkd, polybar, picom, autotile, xcape) without requiring sudo privileges.

- **`init-desktop.sh`**:
  The master desktop startup orchestrator. It ensures 10 workspaces are created, sets the French/Arabic keyboard layouts with `win_space_toggle`, initializes `xcape` for single-tap Super menu, and safely launches or reloads all desktop daemons in detached sessions (`setsid`).

- **`install.sh`**:
  The full system installation script for new machines or clean installs. It installs all APT packages, fonts, themes, Starship prompt, Micro editor, Lazygit, Antigravity CLI (`agy`), deploys all configurations, and applies desktop and system keyboard settings.

- **`duckdns-update.sh`**:
  Queries the current public IP address and securely sends an update request to DuckDNS for the configured domain using credentials isolated in environment variables.
