#!/usr/bin/env bash

# Terminate already running bar instances
killall -q polybar 2>/dev/null || true

# Wait until the processes have been shut down
while pgrep -u $UID -x polybar >/dev/null; do sleep 0.2; done

# Launch Polybar using main bar configuration with setsid
DISPLAY=:0.0 setsid polybar main -c "$HOME/.config/polybar/config.ini" </dev/null > /tmp/polybar.log 2>&1 &
