#!/usr/bin/env bash
# DESC: Compile and upload an ESP32 sketch with configurable Port and Board
# USAGE: jyesp32 [-p PORT] [-b BOARD] <path_to_sketch_folder>

set -euo pipefail

# --- Default Configuration ---
# Default to the most common port if none is specified
DEFAULT_PORT="/dev/ttyUSB0"
# Default to Generic ESP32 if none is specified
DEFAULT_BOARD="esp32:esp32:esp32"

# Initialize variables with defaults
PORT="$DEFAULT_PORT"
BOARD="$DEFAULT_BOARD"

# --- Help Function ---
jyhelp_esp() {
    echo "Usage: jyesp32 [-p PORT] [-b BOARD_FQBN] [SKETCH_PATH]"
    echo ""
    echo "Arguments:"
    echo "  SKETCH_PATH       Path to the folder containing the .ino file"
    echo ""
    echo "Options:"
    echo "  -p <port>         Override port (Default: $DEFAULT_PORT)"
    echo "  -b <fqbn>         Override board FQBN (Default: $DEFAULT_BOARD)"
    echo "  -h                Show this help message"
    echo ""
    echo "Examples:"
    echo "  jyesp32 ~/MySketch                        # Uses default ttyUSB0"
    echo "  jyesp32 -p /dev/ttyACM1 ~/MySketch        # Targets the S3 on ACM1"
    echo "  jyesp32 -p /dev/ttyACM1 -b esp32:esp32:esp32s3 ~/MySketch"
}

# --- Parse Flags (getopts) ---
# This loop looks for -p, -b, and -h flags
while getopts ":p:b:h" opt; do
  case ${opt} in
    p)
      PORT="$OPTARG"
      ;;
    b)
      BOARD="$OPTARG"
      ;;
    h)
      jyhelp_esp
      exit 0
      ;;
    \?)
      echo "[!] Invalid option: -$OPTARG" >&2
      jyhelp_esp
      exit 1
      ;;
    :)
      echo "[!] Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Shift off the options/flags so $1 becomes the sketch path again
shift $((OPTIND -1))

# --- Main Logic ---

# Check if a sketch path was provided after the flags
if [ -z "${1:-}" ]; then
    echo "[!] Error: Missing sketch path."
    jyhelp_esp
    exit 1
fi

SKETCH_PATH="$1"

# 1. Check if the directory exists
if [ ! -d "$SKETCH_PATH" ]; then
    echo "[!] Error: Directory $SKETCH_PATH not found."
    exit 1
fi

echo "=========================================="
echo "[*] Configuration:"
echo "    Sketch: $SKETCH_PATH"
echo "    Board:  $BOARD"
echo "    Port:   $PORT"
echo "=========================================="

# 2. Compile (Verification step)
echo "[*] Compiling sketch..."
if arduino-cli compile --fqbn "$BOARD" "$SKETCH_PATH"; then
    echo "    -> Compilation successful!"
else
    echo "[!] Error: Compilation failed."
    exit 1
fi

# 3. Upload
echo "[*] Uploading..."
if arduino-cli upload -p "$PORT" --fqbn "$BOARD" --verify "$SKETCH_PATH"; then
    echo "[*] Success! Sketch is running."
else
    echo "[!] Error: Upload failed."
    echo "    Check connections to $PORT or hold 'BOOT' button."
    exit 1
fi
