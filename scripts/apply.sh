#!/usr/bin/env bash
# ==============================================================================
# MyEnvMint - Quick Apply & Reload Script
# Synchronizes changes made in this repository to ~/.config/ and reloads daemons.
# ==============================================================================

set -e

export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "==> Synchronizing configuration files from $SCRIPT_DIR..."

# Copy Sxhkd
cp -r "$SCRIPT_DIR/config/sxhkd/"* "$HOME/.config/sxhkd/"
chmod +x "$HOME/.config/sxhkd/scripts/"*.py

# Copy Polybar
cp -r "$SCRIPT_DIR/config/polybar/"* "$HOME/.config/polybar/"
chmod +x "$HOME/.config/polybar/launch.sh"
chmod +x "$HOME/.config/polybar/scripts/"*.py

# Copy Picom
cp "$SCRIPT_DIR/config/picom/picom.conf" "$HOME/.config/picom/picom.conf"

# Copy Starship & Zsh & PowerShell
cp "$SCRIPT_DIR/config/starship/starship.toml" "$HOME/.config/starship.toml"
cp "$SCRIPT_DIR/config/zsh/zshrc" "$HOME/.zshrc"
cp "$SCRIPT_DIR/config/zsh/zshenv" "$HOME/.zshenv" 2>/dev/null || true
mkdir -p "$HOME/.config/powershell"
cp "$SCRIPT_DIR/config/powershell/Microsoft.PowerShell_profile.ps1" "$HOME/.config/powershell/Microsoft.PowerShell_profile.ps1" 2>/dev/null || true

# Copy Micro Editor Config & Plugins
mkdir -p "$HOME/.config/micro/plug"
cp "$SCRIPT_DIR/config/micro/bindings.json" "$HOME/.config/micro/bindings.json" 2>/dev/null || true
cp "$SCRIPT_DIR/config/micro/settings.json" "$HOME/.config/micro/settings.json" 2>/dev/null || true
cp -r "$SCRIPT_DIR/config/micro/plug/"* "$HOME/.config/micro/plug/" 2>/dev/null || true

# Copy Barrier Config
mkdir -p "$HOME/.config/Debauchee"
cp "$SCRIPT_DIR/config/barrier/Barrier.conf" "$HOME/.config/Debauchee/Barrier.conf" 2>/dev/null || true

# Copy Lazygit & Ranger & Xed
mkdir -p "$HOME/.config/lazygit" "$HOME/.config/ranger" "$HOME/.config/xed"
cp -r "$SCRIPT_DIR/config/lazygit/"* "$HOME/.config/lazygit/" 2>/dev/null || true
cp -r "$SCRIPT_DIR/config/ranger/"* "$HOME/.config/ranger/" 2>/dev/null || true
cp -r "$SCRIPT_DIR/config/xed/"* "$HOME/.config/xed/" 2>/dev/null || true

# Copy XFCE & Cinnamon Configs
mkdir -p "$HOME/.config/xfce4/xfconf/xfce-perchannel-xml" "$HOME/.config/xfce4/panel" "$HOME/.config/cinnamon/spices"
cp -r "$SCRIPT_DIR/config/xfce4/xfconf/xfce-perchannel-xml/"* "$HOME/.config/xfce4/xfconf/xfce-perchannel-xml/" 2>/dev/null || true
cp -r "$SCRIPT_DIR/config/xfce4/panel/"* "$HOME/.config/xfce4/panel/" 2>/dev/null || true
cp -r "$SCRIPT_DIR/config/cinnamon/spices/"* "$HOME/.config/cinnamon/spices/" 2>/dev/null || true

# Copy Antigravity CLI & IDE Global Instructions & Settings
mkdir -p "$HOME/.gemini/config/rules" "$HOME/.gemini/antigravity-cli"
cp "$SCRIPT_DIR/config/antigravity/GEMINI.md" "$HOME/.gemini/config/GEMINI.md" 2>/dev/null || true
cp "$SCRIPT_DIR/config/antigravity/AGENTS.md" "$HOME/.gemini/config/AGENTS.md" 2>/dev/null || true
cp "$SCRIPT_DIR/config/antigravity/GEMINI.md" "$HOME/.gemini/GEMINI.md" 2>/dev/null || true
cp "$SCRIPT_DIR/config/antigravity/AGENTS.md" "$HOME/.gemini/AGENTS.md" 2>/dev/null || true
cp "$SCRIPT_DIR/config/antigravity/GEMINI.md" "$HOME/.gemini/config/rules/global-rules.md" 2>/dev/null || true
[ -f "$HOME/.gemini/antigravity-cli/settings.json" ] || cp "$SCRIPT_DIR/config/antigravity/settings.json" "$HOME/.gemini/antigravity-cli/settings.json" 2>/dev/null || true

# Clean up legacy redundant autostart entries to prevent duplicate daemons
rm -f "$HOME/.config/autostart/autotile.desktop" \
      "$HOME/.config/autostart/picom.desktop" \
      "$HOME/.config/autostart/polybar.desktop" \
      "$HOME/.config/autostart/sxhkd.desktop" \
      "$HOME/.config/autostart/xcape.desktop"

# Copy Autostart entries
cp "$SCRIPT_DIR/config/autostart/"*.desktop "$HOME/.config/autostart/"

# Copy Xmodmap & Systemd user units (Barrier & DuckDNS)
cp "$SCRIPT_DIR/config/xmodmap/Xmodmap" "$HOME/.Xmodmap" 2>/dev/null || true
mkdir -p "$HOME/.config/systemd/user" "$HOME/.config/myenvmint/scripts"
cp "$SCRIPT_DIR/config/systemd/user/"* "$HOME/.config/systemd/user/" 2>/dev/null || true
cp "$SCRIPT_DIR/scripts/duckdns-update.sh" "$HOME/.config/myenvmint/scripts/duckdns-update.sh" 2>/dev/null || true
chmod +x "$HOME/.config/myenvmint/scripts/duckdns-update.sh" 2>/dev/null || true
systemctl --user daemon-reload 2>/dev/null || true
systemctl --user enable --now keepalive.service 2>/dev/null || true
if [ -f "$HOME/.config/duckdns/duckdns.env" ] || [ -f "$SCRIPT_DIR/.env" ]; then
    systemctl --user enable --now duckdns.timer 2>/dev/null || true
fi

# Copy xprofile & Master Orchestrator
cp "$SCRIPT_DIR/config/xprofile" "$HOME/.xprofile"
chmod +x "$HOME/.xprofile"
cp "$SCRIPT_DIR/scripts/init-desktop.sh" "$HOME/.config/myenvmint/init-desktop.sh"
chmod +x "$HOME/.config/myenvmint/init-desktop.sh"

# Apply desktop keyboard shortcuts & Whisker Menu settings
if command -v xfconf-query >/dev/null 2>&1; then
    xfconf-query -c keyboard-layout -p /Default/XkbOptions/Group -s "grp:win_space_toggle" 2>/dev/null || true
    xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/Super_L" -n -t string -s "/bin/true" 2>/dev/null || true
    xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/<Super>F1" -n -t string -s "xfce4-popup-whiskermenu" 2>/dev/null || true
    for k in KP_End KP_Down KP_Next KP_Left KP_Begin KP_Right KP_Home KP_Up KP_Page_Up KP_Insert; do
        xfconf-query -c xfce4-keyboard-shortcuts -p "/xfwm4/custom/<Super>$k" -r 2>/dev/null || true
    done
    xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/<Super><Shift>s" -r 2>/dev/null || true
    xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/<Super><Shift>S" -r 2>/dev/null || true
    xfconf-query -c xfce4-panel -p /panels/panel-1/position -n -t string -s "p=10;x=0;y=0" 2>/dev/null || true
    xfconf-query -c xfce4-panel -p /panels/panel-1/autohide-behavior -n -t uint -s 2 2>/dev/null || true
    xfconf-query -c xfce4-panel -p /panels/panel-1/position-locked -n -t bool -s true 2>/dev/null || true
    xfconf-query -c xfce4-panel -p /panels/panel-1/length -n -t uint -s 100 2>/dev/null || true
    xfconf-query -c xfce4-panel -p /plugins/plugin-1 -n -t string -s "whiskermenu" 2>/dev/null || true
    DISPLAY=:0 xfce4-panel -r 2>/dev/null || true
fi
if command -v dconf >/dev/null 2>&1; then
    dconf write /org/cinnamon/menu-key-binding "'<Super>F1'" 2>/dev/null || true
    dconf write /org/cinnamon/desktop/keybindings/wm/panel-main-menu "['<Super>F1']" 2>/dev/null || true
    dconf write /org/cinnamon/desktop/keybindings/media-keys/area-screenshot-clip "['<Super><Shift>s', '<Super><Shift>S', '<Control><Shift>Print']" 2>/dev/null || true
fi

echo "==> Reloading running daemons..."
/bin/bash "$HOME/.config/myenvmint/init-desktop.sh"

echo "==> Applied changes and reloaded all components successfully!"
