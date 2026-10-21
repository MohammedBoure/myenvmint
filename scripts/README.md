# Scripts Directory (`scripts/`)

This directory contains the core management, deployment, and orchestration shell scripts for the MyEnvMint environment.

## Files & Purposes

- **`apply.sh`**:
  Synchronizes configuration files from this repository directly into the user's home configuration (`~/.config/`, `~/.zshrc`, `~/.gemini/`, etc.), enforces bottom panel autohide, Whisker Menu integration, releases conflicting xfwm4 keypad workspace grabs, and immediately reloads all active daemons (sxhkd, polybar, picom, autotile, xcape, xfce4-panel) without requiring sudo privileges.

- **`init-desktop.sh`**:
  The master desktop startup orchestrator. It ensures 10 workspaces are created, sets the French/Arabic keyboard layouts with `win_space_toggle` (strictly 2 layouts without extra groups), configures bottom panel autohide, Whisker Menu bindings, suppresses conflicting window manager key grabs, initializes `xcape` for single-tap Super menu, and safely launches or reloads all desktop daemons in detached sessions (`setsid`).

- **`install.sh`**:
  The full system installation script for new machines or clean installs. It installs all APT packages, fonts, themes, Starship prompt, Micro editor, Lazygit, Zellij Terminal Multiplexer, Antigravity CLI (`agy`), deploys all configurations, and applies desktop and system keyboard settings.


- **`duckdns-update.sh`**:
  Queries the current public IP address and securely sends an update request to DuckDNS for the configured domain using credentials isolated in environment variables.

- **`start`**:
  Windows/macOS-style launcher utility for Linux. Opens directories, files, or URLs in the default desktop file manager (Nemo/Thunar) or application. Automatically defaults to the current working directory (`.`) if invoked without arguments in a fully detached background process.

- **`speed-translate`**:
  CLI and GUI launcher utility for high-speed Arabic-to-English translation. Can be invoked with arguments (`speed-translate "نص"`) to print and copy translations from the terminal, or invoked without arguments to trigger the ultra-fast resident GTK3 dialog and automatic window paste workflow.

- **`osc52`**:
  OSC 52 ANSI control sequence clipboard helper for remote SSH sessions and terminal multiplexers. Encodes stdin into base64 and forwards it directly to the local terminal emulator clipboard over SSH.

- **`sessionx`**:
  Interactive fuzzy-finder session manager for Zellij (installed to `~/.local/bin/sessionx`). Lists all active and exited sessions with visual indicators (`[CURRENT]`, `[ACTIVE]`, `[EXITED]`), and provides rapid single-key actions for attach/switch (`Enter`), rename (`Ctrl + r`), kill (`Ctrl + x` / `Ctrl + d`), and creating new sessions (`Ctrl + n`).

- **`zellij`**:
  Smart binary wrapper installed to `~/.local/bin/zellij` managing the underlying `zellij-bin` executable. Prevents unwanted session creation upon startup, supports intuitive `new`/`create` subcommands (`zellij new <name>`), automatically attaches to single active sessions, opens SessionX when multiple sessions exist, and prompts for explicit confirmation before creating a session when none exist.

- **`agys`**:
  Multi-instance orchestrator and manager for the Antigravity CLI (`agy`). Installed to `~/.local/bin/agys`, it dynamically manages independent, fully isolated environments (`~/.gemini`) for arbitrary instances (`agy1`, `agy2`, ..., `agyN`) using Bubblewrap (`bwrap`) filesystem sandboxing. Provides commands to list active instances (`agys -l`), inspect collective quota and usage limits with dual visual progress bars (both 5-hour rolling limits and weekly quotas with exact reset countdowns matching Antigravity's internal quota windows) across all accounts (`agys -u` / `agys -usage`), run explicit instances (`agys -r <N>`), or delete instances (`agys -d <N>`). Fresh instances automatically inherit global instructions (`GEMINI.md`, `AGENTS.md`) while maintaining separate sessions, credentials, and conversation histories.



