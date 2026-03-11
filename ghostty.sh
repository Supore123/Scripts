#!/bin/bash
# DESC: Launches Ghostty with: Left (Shell), Top-Right (htop), Bottom-Right (neofetch)

# Helper: focus + activate window and wait
focus_ghostty() {
    xdotool windowfocus --sync "$WID"
    xdotool windowactivate --sync "$WID"
    sleep 0.2
}

# 1. Launch Ghostty and capture its PID
ghostty &
GHOSTTY_PID=$!

# 2. Poll until Ghostty's window appears (up to 10s)
WID=""
ATTEMPTS=0
while [ -z "$WID" ] && [ "$ATTEMPTS" -lt 20 ]; do
    sleep 0.5
    WID=$(xdotool search --pid "$GHOSTTY_PID" --onlyvisible 2>/dev/null | head -1)
    ATTEMPTS=$((ATTEMPTS + 1))
done

if [ -z "$WID" ]; then
    echo "Error: Could not find Ghostty window" >&2
    exit 1
fi

# 3. Initial focus
focus_ghostty
sleep 0.1
focus_ghostty
xdotool key alt+Left
sleep 0.1
focus_ghostty
xdotool type "jymatrix"
xdotool key Return

# 4. Split right → htop (top-right pane)
focus_ghostty
xdotool key ctrl+shift+9
sleep 0.2
focus_ghostty
xdotool type "htop"
xdotool key Return

# 5. Split down → neofetch (bottom-right pane)
sleep 0.1
focus_ghostty
xdotool key ctrl+shift+0
sleep 0.2
focus_ghostty
xdotool type "neofetch"
xdotool key Return
xdotool key alt+Left


