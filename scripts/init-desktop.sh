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

# 3. Launch Dual-Role Modifier Daemon (xcape: solo Win tap opens menu, combo acts as modifier)
killall -q xcape 2>/dev/null || true
sleep 0.2
setsid xcape -e 'Super_L=Super_L|F1' </dev/null >/dev/null 2>&1 &

# 4. Launch Keybindings Daemon (sxhkd)
killall -q sxhkd 2>/dev/null || true
sleep 0.2
setsid /usr/bin/sxhkd -c "$HOME/.config/sxhkd/sxhkdrc" </dev/null >/tmp/sxhkd.log 2>&1 &

# 5. Launch Compositor (picom with GLX & white focus highlight)
killall -q picom 2>/dev/null || true
sleep 0.2
picom -b --config "$HOME/.config/picom/picom.conf" >/tmp/picom.log 2>&1

# 6. Launch Polybar
bash "$HOME/.config/polybar/launch.sh" </dev/null >/dev/null 2>&1 &

# 7. Launch Autotiling Daemon
if [ -f /tmp/autotile.pid ]; then
    kill -9 $(cat /tmp/autotile.pid) 2>/dev/null || true
    rm -f /tmp/autotile.pid
fi
sleep 0.2
python3 "$HOME/.config/sxhkd/scripts/autotile.py"
