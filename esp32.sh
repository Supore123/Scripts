#!/usr/bin/env bash
# DESC: ESP32 Manager with Turbo Mode & Flash-Only support
# USAGE: jyesp32 [-p PORT] [-b BOARD] [-f] [-m] <path_to_sketch_folder>

set -euo pipefail

DEFAULT_PORT="/dev/ttyUSB0"
DEFAULT_BOARD="esp32:esp32:esp32"

# Flags
CLEAN_BUILD=false
MONITOR=false
FLASH_ONLY=false

# Help Function
jyhelp_esp() {
    echo "Usage: jyesp32 [-p PORT] [-b BOARD] [-f] [-m] [SKETCH_PATH]"
    echo "  -p <port>   Override port"
    echo "  -b <fqbn>   Override board"
    echo "  -f          Flash only (Skip compile, use existing build)"
    echo "  -c          Clean build (Force re-compile)"
    echo "  -m          Open Serial Monitor after upload"
    echo "  -h          Show help"
}

# Parse Flags
while getopts ":p:b:cfmh" opt; do
  case ${opt} in
    p) PORT="$OPTARG" ;;
    b) BOARD="$OPTARG" ;;
    c) CLEAN_BUILD=true ;;
    f) FLASH_ONLY=true ;;
    m) MONITOR=true ;;
    h) jyhelp_esp; exit 0 ;;
    \?) echo "[!] Invalid option: -$OPTARG" >&2; exit 1 ;;
  esac
done
shift $((OPTIND -1))

# Set Defaults if not provided
PORT="${PORT:-$DEFAULT_PORT}"
BOARD="${BOARD:-$DEFAULT_BOARD}"

SKETCH_PATH="${1:-}"
if [ -z "$SKETCH_PATH" ]; then
    echo "[!] Error: Missing sketch path."
    exit 1
fi

# Determine Build Directory
SAFE_BOARD_NAME=$(echo "$BOARD" | tr ':' '_')
BUILD_DIR="$SKETCH_PATH/build/$SAFE_BOARD_NAME"

echo "=========================================="
echo "[*] Configuration:"
echo "    Sketch:  $SKETCH_PATH"
echo "    Mode:    $( [ "$FLASH_ONLY" = "true" ] && echo "Flash Only (Skip Compile)" || echo "Compile & Upload" )"
echo "    Cache:   $BUILD_DIR"
echo "=========================================="

# 1. Compile (Only if NOT in Flash-Only mode)
if [ "$FLASH_ONLY" = "false" ]; then
    # Handle Clean Build
    if [ "$CLEAN_BUILD" = "true" ]; then
        echo "[*] Cleaning old build files..."
        rm -rf "$BUILD_DIR"
    fi
    mkdir -p "$BUILD_DIR"

    echo "[*] Compiling..."
    if arduino-cli compile --fqbn "$BOARD" --build-path "$BUILD_DIR" "$SKETCH_PATH"; then
        echo "    -> Compilation successful!"
    else
        echo "[!] Error: Compilation failed."
        exit 1
    fi
else
    # Check if build files actually exist before trying to flash
    if [ ! -f "$BUILD_DIR/$SKETCH_PATH.bin" ] && [ ! -f "$BUILD_DIR/$(basename "$SKETCH_PATH").ino.bin" ]; then
        echo "[!] Error: No compiled binary found in $BUILD_DIR"
        echo "    Run without -f first to compile."
        exit 1
    fi
fi

# 2. Upload
echo "[*] Uploading..."
if arduino-cli upload -p "$PORT" --fqbn "$BOARD" --input-dir "$BUILD_DIR" "$SKETCH_PATH"; then
    echo "[*] Success! Sketch is running."
else
    echo "[!] Error: Upload failed."
    exit 1
fi

# 3. Monitor
if [ "$MONITOR" = "true" ]; then
    echo "[*] Opening Monitor..."
    sleep 1
    arduino-cli monitor -p "$PORT" --config baudrate=115200
fi
