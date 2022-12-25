#!/usr/bin/env bash

# Terminate already running bar instances
# If all your bars have ipc enabled, you can use 
polybar-msg cmd quit
# Otherwise you can use the nuclear option:
# killall -q polybar

# Launch bar

tray_output=DisplayPort-0

for m in $(polybar --list-monitors | cut -d":" -f1); do
    tray_position=none
    if [[ $m == $tray_output ]]; then
	tray_position=right
    fi
    MONITOR=$m TRAY_POSITION=$tray_position polybar mybar &
done

echo "Bars launched..."
