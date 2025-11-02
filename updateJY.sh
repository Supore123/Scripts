#!/usr/bin/env bash
# update-commands.sh — copy all scripts in this folder to /usr/local/bin
# Adds a 'JY' prefix to each global command name.

set -euo pipefail

SCRIPTS_DIR="$(dirname "$(realpath "$0")")"

echo "[*] Updating global commands from $SCRIPTS_DIR..."

for script in "$SCRIPTS_DIR"/*.sh; do
  [ -f "$script" ] || continue

  # Extract base name without extension
  base_name="$(basename "$script" .sh)"
  name="JY${base_name}"
  target="/usr/local/bin/$name"

  echo "   → Installing as $name ..."
  sudo cp "$script" "$target"
  sudo chmod +x "$target"
done

echo "[*] All scripts updated successfully! Now use them as JY<commandname>."
