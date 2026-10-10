# Configuration Directory (`config/`)

This directory houses all user configuration bundles and dotfiles that define the MyEnvMint desktop environment.

## Subdirectories & Modules

- **`sxhkd/`**: X11 shortcut daemon configuration (`sxhkdrc`) and Python window management scripts.
- **`polybar/`**: Top bar configuration (`config.ini`), launch script, and live telemetry scripts.
- **`picom/`**: Compositor configuration (`picom.conf`) providing 2px active window white borders and subtle background dimming.
- **`starship/`**: Starship prompt preset (`starship.toml`).
- **`zsh/`**: Zsh shell configuration (`zshrc`).
- **`micro/`**: Micro editor configurations (`bindings.json`, `settings.json`, and productivity plugins including `filemanager`, `fzf`, `editorconfig`, `bookmark`, `snippets`).
- **`barrier/`**: KVM mouse and keyboard network sharing configuration (`Barrier.conf`).
- **`lazygit/`**: Lazygit terminal UI configuration (`config.yml`).
- **`ranger/`**: Ranger console file manager configuration.
- **`xed/`**: Text editor keyboard accelerators (`accels`).
- **`xfce4/`**: XFCE panel and xfconf per-channel XML files (terminal colors, multi-monitor display profiles, window manager).
- **`cinnamon/`**: Cinnamon spice applet configurations (sound, power, network, menu).
- **`autostart/`**: Desktop entry autostart launchers deployed to `~/.config/autostart/`.
- **`antigravity/`**: Antigravity CLI and IDE global instructions (`GEMINI.md`, `AGENTS.md`) and settings.
- **`xmodmap/`**: X11 keycode mappings fixing Barrier Arabic typing (`Xmodmap`).
- **`systemd/`**: User systemd unit services (`barrier-client.service`).
- **`xprofile`**: X11 session login script invoking `init-desktop.sh`.
