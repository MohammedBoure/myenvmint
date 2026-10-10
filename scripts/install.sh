#!/usr/bin/env bash
# ==============================================================================
# MyEnvMint - Complete Installation & Deployment Script
# Automatically configures:
#   - GlazeWM-style tiling, Polybar, Picom
#   - Zsh & Starship Shell
#   - Micro Editor + Plugins, Lazygit, Ranger
#   - Barrier KVM, Moonlight, XFCE & Cinnamon desktop settings
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "==> Deploying MyEnvMint from: $SCRIPT_DIR"

# 1. Install prerequisites via apt
echo "==> Step 1: Installing system packages via apt..."
sudo apt-get update
sudo apt-get install -y \
    sxhkd wmctrl xdotool jq polybar picom xcape vnstat \
    zsh git curl fzf ranger barrier moonlight-qt \
    fonts-jetbrains-mono fonts-firacode fonts-font-awesome papirus-icon-theme

# 2. Enable vnstat daemon for daily traffic calculation
sudo systemctl enable --now vnstat

# 3. Install Starship prompt if missing
if ! command -v starship >/dev/null 2>&1; then
    echo "==> Step 2: Installing Starship prompt..."
    curl -sS https://starship.rs/install.sh | sudo sh -s -- -y
fi

# 4. Install Micro Text Editor if missing
if ! command -v micro >/dev/null 2>&1; then
    echo "==> Step 3: Installing Micro editor..."
    curl -fsSL https://getmic.ro | bash
    sudo mv micro /usr/local/bin/
fi

# 5. Install Lazygit if missing
if ! command -v lazygit >/dev/null 2>&1; then
    echo "==> Step 4: Installing Lazygit..."
    LAZYGIT_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" | grep -Po '"tag_name": "v\K[^"]*')
    curl -Lo lazygit.tar.gz "https://github.com/jesseduffield/lazygit/releases/latest/download/lazygit_${LAZYGIT_VERSION}_Linux_x86_64.tar.gz"
    tar xf lazygit.tar.gz lazygit
    sudo install lazygit /usr/local/bin
    rm -f lazygit lazygit.tar.gz
fi

# 6. Clone Zsh plugins if missing
echo "==> Step 5: Setting up Zsh plugins..."
mkdir -p "$HOME/.zsh"
[ -d "$HOME/.zsh/zsh-autosuggestions" ] || git clone https://github.com/zsh-users/zsh-autosuggestions "$HOME/.zsh/zsh-autosuggestions"
[ -d "$HOME/.zsh/zsh-syntax-highlighting" ] || git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "$HOME/.zsh/zsh-syntax-highlighting"

# 7. Set default shell to Zsh
if [ "$SHELL" != "$(which zsh)" ]; then
    echo "==> Step 6: Setting Zsh as default user shell..."
    sudo chsh -s "$(which zsh)" "$USER"
fi

# 8. Check and install Antigravity CLI (agy) if not present
if ! command -v agy >/dev/null 2>&1 && [ ! -f "$HOME/.local/bin/agy" ]; then
    echo "==> Step 7: Installing Antigravity CLI (agy)..."
    curl -fsSL https://antigravity.google/cli/install.sh | bash
else
    echo "==> Antigravity CLI (agy) is already installed."
fi

# 9. Deploy all user configuration files
echo "==> Step 8: Deploying configuration files..."
mkdir -p "$HOME/.config/sxhkd/scripts"
mkdir -p "$HOME/.config/polybar/scripts"
mkdir -p "$HOME/.config/picom"
mkdir -p "$HOME/.config/autostart"
mkdir -p "$HOME/.config/micro/plug"
mkdir -p "$HOME/.config/Debauchee"
mkdir -p "$HOME/.config/lazygit"
mkdir -p "$HOME/.config/ranger"
mkdir -p "$HOME/.config/xed"
mkdir -p "$HOME/.config/myenvmint"
mkdir -p "$HOME/.config/cinnamon/spices"
mkdir -p "$HOME/.config/xfce4/xfconf/xfce-perchannel-xml"
mkdir -p "$HOME/.config/xfce4/panel"

# Sxhkd
cp -r "$SCRIPT_DIR/config/sxhkd/"* "$HOME/.config/sxhkd/"
chmod +x "$HOME/.config/sxhkd/scripts/"*.py

# Polybar
cp -r "$SCRIPT_DIR/config/polybar/"* "$HOME/.config/polybar/"
chmod +x "$HOME/.config/polybar/launch.sh"
chmod +x "$HOME/.config/polybar/scripts/"*.py

# Picom
cp "$SCRIPT_DIR/config/picom/picom.conf" "$HOME/.config/picom/picom.conf"

# Starship & Zsh
cp "$SCRIPT_DIR/config/starship/starship.toml" "$HOME/.config/starship.toml"
cp "$SCRIPT_DIR/config/zsh/zshrc" "$HOME/.zshrc"

# Micro Editor Config & Plugins
cp "$SCRIPT_DIR/config/micro/bindings.json" "$HOME/.config/micro/bindings.json" 2>/dev/null || true
cp "$SCRIPT_DIR/config/micro/settings.json" "$HOME/.config/micro/settings.json" 2>/dev/null || true
cp -r "$SCRIPT_DIR/config/micro/plug/"* "$HOME/.config/micro/plug/" 2>/dev/null || true

# Barrier Config
cp "$SCRIPT_DIR/config/barrier/Barrier.conf" "$HOME/.config/Debauchee/Barrier.conf" 2>/dev/null || true

# Lazygit & Ranger & Xed
cp -r "$SCRIPT_DIR/config/lazygit/"* "$HOME/.config/lazygit/" 2>/dev/null || true
cp -r "$SCRIPT_DIR/config/ranger/"* "$HOME/.config/ranger/" 2>/dev/null || true
cp -r "$SCRIPT_DIR/config/xed/"* "$HOME/.config/xed/" 2>/dev/null || true

# XFCE & Cinnamon Configs
cp -r "$SCRIPT_DIR/config/xfce4/xfconf/xfce-perchannel-xml/"* "$HOME/.config/xfce4/xfconf/xfce-perchannel-xml/" 2>/dev/null || true
cp -r "$SCRIPT_DIR/config/xfce4/panel/"* "$HOME/.config/xfce4/panel/" 2>/dev/null || true
cp -r "$SCRIPT_DIR/config/cinnamon/spices/"* "$HOME/.config/cinnamon/spices/" 2>/dev/null || true

# Antigravity CLI & IDE Global Instructions & Settings
mkdir -p "$HOME/.gemini/config/rules" "$HOME/.gemini/antigravity-cli"
cp "$SCRIPT_DIR/config/antigravity/GEMINI.md" "$HOME/.gemini/config/GEMINI.md" 2>/dev/null || true
cp "$SCRIPT_DIR/config/antigravity/AGENTS.md" "$HOME/.gemini/config/AGENTS.md" 2>/dev/null || true
cp "$SCRIPT_DIR/config/antigravity/GEMINI.md" "$HOME/.gemini/GEMINI.md" 2>/dev/null || true
cp "$SCRIPT_DIR/config/antigravity/AGENTS.md" "$HOME/.gemini/AGENTS.md" 2>/dev/null || true
cp "$SCRIPT_DIR/config/antigravity/GEMINI.md" "$HOME/.gemini/config/rules/global-rules.md" 2>/dev/null || true
[ -f "$HOME/.gemini/antigravity-cli/settings.json" ] || cp "$SCRIPT_DIR/config/antigravity/settings.json" "$HOME/.gemini/antigravity-cli/settings.json" 2>/dev/null || true

# Autostart entries
cp "$SCRIPT_DIR/config/autostart/"*.desktop "$HOME/.config/autostart/"

# xprofile & Master Orchestrator
cp "$SCRIPT_DIR/config/xprofile" "$HOME/.xprofile"
chmod +x "$HOME/.xprofile"
cp "$SCRIPT_DIR/scripts/init-desktop.sh" "$HOME/.config/myenvmint/init-desktop.sh"
chmod +x "$HOME/.config/myenvmint/init-desktop.sh"

# 9. Apply System & Desktop Settings
echo "==> Step 8: Applying system keyboard & desktop settings..."
if [ -f "$SCRIPT_DIR/system/keyboard.conf" ]; then
    sudo cp "$SCRIPT_DIR/system/keyboard.conf" /etc/default/keyboard
    sudo udevadm trigger --subsystem-match=input 2>/dev/null || true
fi

# Apply XFCE desktop settings
if command -v xfconf-query >/dev/null 2>&1; then
    xfconf-query -c keyboard-layout -p /Default/XkbOptions/Group -s "grp:win_space_toggle" 2>/dev/null || true
    xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/Super_L" -r 2>/dev/null || true
    xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/<Super>F1" -n -t string -s "xfce4-popup-whiskermenu" 2>/dev/null || true
fi

# Apply Cinnamon dconf settings
if command -v dconf >/dev/null 2>&1; then
    dconf write /org/cinnamon/menu-key-binding "'<Super>F1'" 2>/dev/null || true
    dconf write /org/cinnamon/desktop/keybindings/wm/panel-main-menu "['<Super>F1']" 2>/dev/null || true
fi

# 10. Start / Reload Desktop Daemons
echo "==> Step 9: Starting all desktop daemons..."
/bin/bash "$HOME/.config/myenvmint/init-desktop.sh"

echo "==> MyEnvMint has been successfully installed, customized, and launched!"
