#!/usr/bin/env bash
# DESC: Compile and upload an ESP32 sketch to /dev/ttyUSB0
# USAGE: jyesp32 <path_to_sketch_folder>

set -euo pipefail

# Configuration
# ESP32s usually appear as ttyUSB* (Arduino Uno is usually ttyACM*)
PORT="/dev/ttyUSB0"
# This is the standard FQBN for a generic ESP32 Dev Module
BOARD="esp32:esp32:esp32"

# Help Function
jyhelp_esp() {
    echo "Usage: jyesp32 [SKETCH_PATH]"
    echo ""
    echo "Arguments:"
    echo "  SKETCH_PATH    Path to the folder containing the .ino file"
    echo ""
    echo "Example:"
    echo "  jyesp32 ~/MyESPProject"
}

# Check for help flag or missing arguments
if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || -z "${1:-}" ]]; then
    jyhelp_esp
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
# Note: ESP32 compilation takes longer than Arduino Uno
if arduino-cli compile --fqbn "$BOARD" "$SKETCH_PATH"; then
    echo "    → Compilation successful!"
else
    echo "[!] Error: Compilation failed. Check your code."
    exit 1
fi

# 3. Upload
echo "[*] Uploading to ESP32..."
# ESP32s sometimes need the --verify flag to ensure flash integrity
if arduino-cli upload -p "$PORT" --fqbn "$BOARD" --verify "$SKETCH_PATH"; then
    echo "[*] Success! Sketch is running."
else
    echo "[!] Error: Upload failed. Is the ESP32 plugged into $PORT?"
    echo "    Note: You may need to hold the 'BOOT' button on the board during 'Connecting...'"
    exit 1
fi
