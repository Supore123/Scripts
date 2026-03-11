#!/bin/bash
# DESC: Launches Ghostty with: Left (Shell), Top-Right (htop), Bottom-Right (neofetch)
# 1. Launch Ghostty
ghostty & 
# 2. Wait a moment for the window to appear
sleep 1.5
# 3. Send your config's split shortcuts
# Based on your config: ctrl+shift+9 is split right
xdotool key ctrl+shift+9
sleep 0.2
xdotool type "htop"
xdotool key Return
# Based on your config: ctrl+shift+0 is split down
xdotool key ctrl+shift+0
sleep 0.2
xdotool type "neofetch"
xdotool key Return
# Move back to the left (alt+left in your config)
xdotool key alt+Left
