#!/usr/bin/env bash
# ==============================================================================
# MyEnvMint Master Desktop Environment Startup Orchestrator
# Ensures all daemons, shortcuts, keymaps, and tiling start reliably on reboot.
# ==============================================================================

export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"
unset WINDOWID
unset DESKTOP_STARTUP_ID

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
setxkbmap -option "" -layout "fr,ara" -variant "azerty," -option "grp:win_space_toggle,terminate:ctrl_alt_bksp" 2>/dev/null || true

# 2b. Apply Arabic Keycode Corrections for Barrier & AZERTY (Jeem and Thal)
xmodmap -e "keycode 18 = ccedilla 9 Arabic_jeem parenright asciicircum NoSymbol Arabic_jeem U062C" 2>/dev/null || true
xmodmap -e "keycode 51 = asterisk mu Arabic_thal bar asterisk mu Arabic_thal U0630" 2>/dev/null || true
xmodmap -e "keycode 197 = Arabic_jeem Arabic_jeem Arabic_jeem Arabic_jeem" 2>/dev/null || true
xmodmap -e "keycode 202 = Arabic_thal Arabic_thal Arabic_thal Arabic_thal" 2>/dev/null || true
systemctl --user restart barrier-client.service 2>/dev/null || true

# 3. Configure Whisker Menu / Cinnamon Menu shortcuts
if command -v xfconf-query >/dev/null 2>&1; then
    xfconf-query -c xfce4-keyboard-shortcuts -p "/commands/custom/Super_L" -r 2>/dev/null || true
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
fi
if command -v dconf >/dev/null 2>&1; then
    dconf write /org/cinnamon/menu-key-binding "'<Super>F1'" 2>/dev/null || true
    dconf write /org/cinnamon/desktop/keybindings/wm/panel-main-menu "['<Super>F1']" 2>/dev/null || true
    dconf write /org/cinnamon/desktop/keybindings/media-keys/area-screenshot-clip "['<Super><Shift>s', '<Super><Shift>S', '<Control><Shift>Print']" 2>/dev/null || true
fi

# 3b. Disable Screen Blanking, DPMS, Screensaver & Sleep (Keep System Always On)
xset s off -dpms 2>/dev/null || true
if command -v xfconf-query >/dev/null 2>&1; then
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/blank-on-ac -s 0 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/blank-on-battery -n -t int -s 0 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/dpms-enabled -s false 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/dpms-on-ac-sleep -s 0 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/dpms-on-ac-off -s 0 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/dpms-on-battery-sleep -s 0 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/dpms-on-battery-off -s 0 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/presentation-mode -n -t bool -s true 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/inactivity-on-ac -n -t uint -s 0 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/inactivity-on-battery -n -t uint -s 0 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/lid-action-on-ac -n -t uint -s 0 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/lid-action-on-battery -s 0 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/power-button-action -n -t uint -s 0 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/sleep-button-action -n -t uint -s 0 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/hibernate-button-action -n -t uint -s 0 2>/dev/null || true
    xfconf-query -c xfce4-power-manager -p /xfce4-power-manager/lock-screen-suspend-hibernate -s false 2>/dev/null || true
fi
if command -v gsettings >/dev/null 2>&1; then
    gsettings set org.cinnamon.settings-daemon.plugins.power sleep-display-ac 0 2>/dev/null || true
    gsettings set org.cinnamon.settings-daemon.plugins.power sleep-display-battery 0 2>/dev/null || true
    gsettings set org.cinnamon.settings-daemon.plugins.power sleep-inactive-ac-timeout 0 2>/dev/null || true
    gsettings set org.cinnamon.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing' 2>/dev/null || true
    gsettings set org.cinnamon.settings-daemon.plugins.power sleep-inactive-battery-timeout 0 2>/dev/null || true
    gsettings set org.cinnamon.settings-daemon.plugins.power sleep-inactive-battery-type 'nothing' 2>/dev/null || true
    gsettings set org.cinnamon.settings-daemon.plugins.power lid-close-ac-action 'nothing' 2>/dev/null || true
    gsettings set org.cinnamon.settings-daemon.plugins.power lid-close-battery-action 'nothing' 2>/dev/null || true
    gsettings set org.cinnamon.settings-daemon.plugins.power button-suspend 'nothing' 2>/dev/null || true
    gsettings set org.cinnamon.settings-daemon.plugins.power button-hibernate 'nothing' 2>/dev/null || true
    gsettings set org.cinnamon.settings-daemon.plugins.power lock-on-suspend false 2>/dev/null || true
    gsettings set org.cinnamon.desktop.session idle-delay 0 2>/dev/null || true
    gsettings set org.cinnamon.desktop.screensaver idle-activation-enabled false 2>/dev/null || true
    gsettings set org.cinnamon.desktop.screensaver lock-enabled false 2>/dev/null || true
fi
systemctl --user enable --now keepalive.service 2>/dev/null || true

# Launch Dual-Role Modifier Daemon (xcape: solo Win tap opens menu, combo acts as modifier)
killall -9 xcape 2>/dev/null || true
sleep 0.2
setsid xcape -t 1000 -e 'Super_L=Super_L|F1;Super_R=Super_L|F1' </dev/null >/dev/null 2>&1 &

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

# 8. Launch Ultra-Fast Speed Translation Daemon
pkill -9 -f "[s]peed_translate.py daemon" 2>/dev/null || true
rm -f /tmp/speed_translate.sock /tmp/speed_translate.pid
sleep 0.1
python3 "$HOME/.config/sxhkd/scripts/speed_translate.py" daemon
