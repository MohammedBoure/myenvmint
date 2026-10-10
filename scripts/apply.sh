#!/usr/bin/env bash
# ==============================================================================
# MyEnvMint - Quick Apply & Reload Script
# Synchronizes changes made in this repository to ~/.config/ and reloads daemons.
# ==============================================================================

set -e

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

# Copy Starship & Zsh
cp "$SCRIPT_DIR/config/starship/starship.toml" "$HOME/.config/starship.toml"
cp "$SCRIPT_DIR/config/zsh/zshrc" "$HOME/.zshrc"

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

# Copy Autostart entries
cp "$SCRIPT_DIR/config/autostart/"*.desktop "$HOME/.config/autostart/"

# Copy xprofile & Master Orchestrator
cp "$SCRIPT_DIR/config/xprofile" "$HOME/.xprofile"
chmod +x "$HOME/.xprofile"
cp "$SCRIPT_DIR/scripts/init-desktop.sh" "$HOME/.config/myenvmint/init-desktop.sh"
chmod +x "$HOME/.config/myenvmint/init-desktop.sh"

echo "==> Reloading running daemons..."
/bin/bash "$HOME/.config/myenvmint/init-desktop.sh"

echo "==> Applied changes and reloaded all components successfully!"
