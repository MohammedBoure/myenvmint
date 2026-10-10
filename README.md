# MyEnvMint - Integrated Linux Mint (X11) Desktop Environment
### GlazeWM-Style Tiling • Polybar Status Bar • Picom Compositor • Zsh & Starship

A comprehensive, fully tracked desktop configuration environment that implements advanced GlazeWM-style tiling on Linux Mint (X11) while preserving core system utilities, the Nemo file manager, Whisker Start Menu, and an autohiding bottom panel.

---

## 📂 Project Structure

```text
/home/pluto/Desktop/myenvmint/
├── config/
│   ├── sxhkd/                    # Keybindings and window management scripts
│   │   ├── sxhkdrc               # Master keybindings definition file
│   │   └── scripts/
│   │       ├── autotile.py       # Automatic window tiling engine (GlazeWM Tiling Daemon)
│   │       ├── focus.py          # Directional window navigation
│   │       ├── window_manage.py  # Window resizing, centering, and movement
│   │       └── open_terminal.py  # Terminal launcher in current active directory
│   ├── polybar/                  # Modern top status bar
│   │   ├── config.ini            # Status bar theme, layout, and module definitions
│   │   ├── launch.sh             # Polybar startup script
│   │   └── scripts/
│   │       └── traffic_today.py  # Cumulative daily network traffic monitor
│   ├── picom/                    # X11 Compositor
│   │   └── picom.conf            # GLX backend, opacity, active border highlight, shadows
│   ├── starship/                 # Terminal prompt styling engine
│   │   └── starship.toml         # Custom Starship prompt configuration
│   ├── zsh/                      # Zsh shell configuration
│   │   └── zshrc                 # Enhanced ~/.zshrc with plugins and aliases
│   ├── micro/                    # Micro editor settings, bindings, and filemanager plugin
│   ├── barrier/                  # Barrier KVM keyboard/mouse sharing client config
│   ├── duckdns/                  # DuckDNS dynamic DNS configuration templates
│   ├── lazygit/                  # Lazygit terminal GUI configuration
│   ├── ranger/                   # Ranger terminal file manager settings
│   ├── xed/                      # Xed text editor shortcuts
│   ├── xfce4/                    # XFCE terminal, multi-monitor, and panel configurations
│   │   └── xfconf/xfce-perchannel-xml/xfce4-panel.xml # Autohiding bottom panel & Whisker Menu
│   ├── cinnamon/                 # Cinnamon desktop and applet settings (spices)
│   ├── antigravity/              # Antigravity CLI and global AI agent rules
│   ├── xmodmap/                  # Custom keymap corrections for Barrier KVM & AZERTY/Arabic
│   ├── systemd/                  # User-level systemd service units (Barrier & DuckDNS)
│   ├── autostart/                # Desktop session autostart entries
│   └── xprofile                  # X11 session environment initialization
├── scripts/
│   ├── init-desktop.sh           # Master desktop startup orchestrator
│   ├── apply.sh                  # Instant configuration sync and daemon reload script
│   ├── install.sh                # Full fresh-system installation script
│   └── duckdns-update.sh         # Dynamic DNS updater script for DuckDNS
├── system/                       # System-level configurations and backups
│   ├── keyboard.conf             # /etc/default/keyboard layout template
│   ├── dconf_cinnamon.ini        # Cinnamon desktop keybindings backup
│   ├── xfconf_keyboard.txt       # XFCE keyboard layout channel export
│   └── xfconf_shortcuts.txt      # Registered XFCE keyboard shortcuts backup
├── .agent/                       # Antigravity AI agent rules and customizations
├── GEMINI.md                     # Authoritative global AI agent instructions
├── AGENTS.md                     # Mirrored AI instructions for universal engine support
└── README.md                     # Comprehensive documentation and usage guide
```

---

## ⌨️ Keybindings

### 1. Directional Window Navigation
| Shortcut | Action |
| :--- | :--- |
| `Alt + h` or `Alt + Left` | Focus window to the left |
| `Alt + l` or `Alt + Right` | Focus window to the right |
| `Alt + k` or `Alt + Up` | Focus window above |
| `Alt + j` or `Alt + Down` | Focus window below |

### 2. Window Management
| Shortcut | Action |
| :--- | :--- |
| `Alt + q` | Gracefully close active window (`WM_DELETE_WINDOW` without killing app) |
| `Alt + f` | Toggle fullscreen mode for active window |
| `Alt + m` | Minimize active window |
| `Alt + Shift + Space` | Center active window on screen |
| `Alt + u` / `Alt + p` | Decrease / Increase window width by 2% |
| `Alt + i` / `Alt + o` | Decrease / Increase window height by 2% |

### 3. Workspaces (1 to 10)
| Shortcut | Action |
| :--- | :--- |
| `Alt + 1..9, 0` or `Alt + & .. à` | Switch to workspace with automatic directional focus (no manual click needed) |
| `Alt + Shift + 1..9, 0` or `Alt + Shift + & .. à` | Move active window to targeted workspace and follow viewport automatically |

### 4. Application Launching, Panel & Layout Switching
| Shortcut / Trigger | Action |
| :--- | :--- |
| `Win (Super)` (single tap) | Open Start Menu (Whisker Menu) |
| `Win + Space` | Instant keyboard layout toggle (French AZERTY / Arabic) without triggering menu |
| `Alt + Ctrl + Enter` | Open modern terminal (Zsh + Starship) |
| `Alt + n` | Open default text editor (Xed) |
| `Alt + Ctrl + t` | Open terminal inside the active Nemo file manager directory |
| Hover at screen bottom | Reveals the autohidden bottom panel (Whisker Menu, tasklist, system tray, clock) |

---

## 🛠️ Customization & Modifications

All configuration files and scripts are located directly inside this workspace:
1. **Modify shortcuts:** Edit `config/sxhkd/sxhkdrc`.
2. **Modify Polybar (colors, modules, layout):** Edit `config/polybar/config.ini`.
3. **Modify terminal appearance:** Edit `config/starship/starship.toml` or `config/zsh/zshrc`.
4. **Modify autotiling gaps & layout:** Edit `config/sxhkd/scripts/autotile.py` (adjust `GAP` and `OUTER_GAP`).
5. **Modify bottom panel behavior:** Edit `config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml`.

To apply changes instantly without requiring root privileges or a session restart, run:
```bash
./scripts/apply.sh
```

---

## 🚀 Installation & Fresh Setup

To replicate or install this desktop environment on a new Linux Mint installation:
1. Copy or clone the `myenvmint` folder to `~/Desktop/myenvmint`.
2. Open a terminal in the folder and execute:
```bash
chmod +x scripts/*.sh
./scripts/install.sh
```
The script automatically installs required APT packages, fonts, themes, terminal tools, deploys configurations, sets up systemd user services, and initializes the environment seamlessly.
