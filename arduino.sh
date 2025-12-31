#!/usr/bin/env bash
# DESC: Compile and upload an Arduino sketch to /dev/ttyACM0
# USAGE: jyuno <path_to_sketch_folder>

set -euo pipefail

# Configuration
PORT="/dev/ttyACM0"
BOARD="arduino:avr:uno"

# Help Function
jyhelp_uno() {
    echo "Usage: jyuno [SKETCH_PATH]"
    echo ""
    echo "Arguments:"
    echo "  SKETCH_PATH    Path to the folder containing the .ino file"
    echo ""
    echo "Example:"
    echo "  jyuno ~/MyProject"
}

# Check for help flag or missing arguments
if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || -z "${1:-}" ]]; then
    jyhelp_uno
    exit 0
fi

SKETCH_PATH="$1"

# 1. Check if the directory exists
if [ ! -d "$SKETCH_PATH" ]; then
    echo "[!] Error: Directory $SKETCH_PATH not found."
    exit 1
fi

echo "[*] Target: $BOARD on $PORT"

# 2. Compile (Verification step)
echo "[*] Compiling and verifying sketch..."
if arduino-cli compile --fqbn "$BOARD" "$SKETCH_PATH"; then
    echo "    → Compilation successful!"
else
    echo "[!] Error: Compilation failed. Check your code."
    exit 1
fi

# 3. Upload
echo "[*] Uploading to Arduino Uno..."
if arduino-cli upload -p "$PORT" --fqbn "$BOARD" "$SKETCH_PATH"; then
    echo "[*] Success! Sketch is running."
else
    echo "[!] Error: Upload failed. Is the Arduino plugged into $PORT?"
    exit 1
fi
