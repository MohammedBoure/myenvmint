# Configuration Directory (`config/`)

This directory houses all user configuration bundles and dotfiles that define the MyEnvMint desktop environment.

## Subdirectories & Modules

- **`sxhkd/`**: X11 shortcut daemon configuration (`sxhkdrc`) and Python window management scripts.
- **`polybar/`**: Top bar configuration (`config.ini`), launch script, and live telemetry scripts.
- **`picom/`**: Compositor configuration (`picom.conf`) providing 3px uniform window outline borders and subtle background dimming.
- **`gtk-3.0/`**: Global GTK3 stylesheet (`gtk.css`) enforcing high-contrast window boundaries across client-side decorated applications.
- **`themes/`**: Custom desktop and window manager themes (`MyEnvMint-Dark/xfwm4`) with dedicated high-contrast active and inactive window frames.
- **`starship/`**: Starship prompt preset (`starship.toml`).
- **`zsh/`**: Zsh shell configuration (`zshrc`).
- **`micro/`**: Micro editor configurations (`bindings.json`, `settings.json`, and productivity plugins including `filemanager`, `fzf`, `editorconfig`, `bookmark`, `snippets`).
- **`zellij/`**: Zellij terminal multiplexer configuration (`config.kdl`) with SessionX session manager integration (`Alt + s` and `Ctrl + o` then `w`).
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
