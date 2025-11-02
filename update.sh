#!/usr/bin/env bash
# DESC: Copy all scripts in this folder to /usr/local/bin as JY-prefixed commands

set -euo pipefail

SCRIPTS_DIR="$(dirname "$(realpath "$0")")"

echo "[*] Updating global JY commands from $SCRIPTS_DIR..."

for script in "$SCRIPTS_DIR"/*.sh; do
  [ -f "$script" ] || continue

  # Extract base name without extension
  base_name="$(basename "$script" .sh)"

  # Automatically determine the JY command name
  # If the script is this update script itself, always call it JYupdate
  if [ "$base_name" == "$(basename "$0" .sh)" ]; then
    name="JYupdate"
  else
    name="JY${base_name}"
  fi

  target="/usr/local/bin/$name"

  # Remove old version if it exists
  if [ -f "$target" ]; then
    sudo rm "$target"
  fi

  echo "   → Installing $name ..."
  sudo cp "$script" "$target"
  sudo chmod +x "$target"
done

# Print summary of installed JY commands
echo "[*] Installed JY commands:"
ls /usr/local/bin | grep '^JY' | sort

echo "[*] All scripts updated successfully! You can now run them anywhere using JY<commandname>."
