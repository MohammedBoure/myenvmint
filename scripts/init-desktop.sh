#!/usr/bin/env bash
# ==============================================================================
# MyEnvMint Master Desktop Environment Startup Orchestrator
# Ensures all daemons, shortcuts, keymaps, and tiling start reliably on reboot.
# ==============================================================================

# Wait for X display to become ready
count=0
while ! xset q >/dev/null 2>&1; do
    sleep 0.2
    count=$((count+1))
    if [ $count -gt 50 ]; then
        break
    fi
done

# Small settling delay for window manager to register
sleep 0.5

# 1. Ensure 10 Workspaces exist in EWMH
wmctrl -n 10 2>/dev/null || true

# 2. Configure System Keyboard Layout (FR AZERTY + Arabic, Win+Space toggle)
setxkbmap -layout "fr,ara" -variant "azerty," -option "grp:win_space_toggle,terminate:ctrl_alt_bksp" 2>/dev/null || true

# 2b. Apply Arabic Keycode Corrections for Barrier & AZERTY (Jeem and Thal)
xmodmap -e "keycode 18 = ccedilla 9 9 parenright asciicircum NoSymbol" 2>/dev/null || true
xmodmap -e "keycode 51 = asterisk mu backslash bar asterisk mu" 2>/dev/null || true
xmodmap -e "keycode 197 = Arabic_jeem Arabic_jeem Arabic_jeem Arabic_jeem" 2>/dev/null || true
xmodmap -e "keycode 202 = Arabic_thal Arabic_thal Arabic_thal Arabic_thal" 2>/dev/null || true
systemctl --user restart barrier-client.service 2>/dev/null || true

# 3. Configure Whisker Menu / Cinnamon Menu shortcuts (suppress keydown Super trigger)
if command -v xfconf-query >/dev/null 2>&1; then
    xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/Super_L" -n -t string -s "/bin/true" 2>/dev/null || true
    xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/<Super>F1" -n -t string -s "xfce4-popup-whiskermenu" 2>/dev/null || true
fi
if command -v dconf >/dev/null 2>&1; then
    dconf write /org/cinnamon/menu-key-binding "'<Super>F1'" 2>/dev/null || true
    dconf write /org/cinnamon/desktop/keybindings/wm/panel-main-menu "['<Super>F1']" 2>/dev/null || true
fi

# Launch Dual-Role Modifier Daemon (xcape: solo Win tap opens menu, combo acts as modifier)
killall -9 xcape 2>/dev/null || true
sleep 0.2
setsid xcape -e 'Super_L=Super_L|F1' </dev/null >/dev/null 2>&1 &

# 4. Launch Keybindings Daemon (sxhkd)
killall -9 sxhkd 2>/dev/null || true
sleep 0.2
setsid /usr/bin/sxhkd -m -1 -c "$HOME/.config/sxhkd/sxhkdrc" </dev/null >/tmp/sxhkd.log 2>&1 &

# 5. Launch Compositor (picom with GLX & white focus highlight)
killall -9 picom 2>/dev/null || true
sleep 0.2
picom -b --config "$HOME/.config/picom/picom.conf" >/tmp/picom.log 2>&1

# 6. Launch Polybar
bash "$HOME/.config/polybar/launch.sh" </dev/null >/dev/null 2>&1 &

# 7. Launch Autotiling Daemon
pkill -9 -f "autotile.py" 2>/dev/null || true
rm -f /tmp/autotile.pid
sleep 0.2
python3 "$HOME/.config/sxhkd/scripts/autotile.py"
