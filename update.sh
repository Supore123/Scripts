#!/usr/bin/env bash
# DESC: Copy all scripts in this folder to /usr/local/bin as JY-prefixed commands
#       Also creates a global 'JY' command that runs JYhelp

set -euo pipefail

SCRIPTS_DIR="$(dirname "$(realpath "$0")")"

echo "[*] Updating global JY commands from $SCRIPTS_DIR..."

for script in "$SCRIPTS_DIR"/*.sh; do
  [ -f "$script" ] || continue

  # Extract base name without extension
  base_name="$(basename "$script" .sh)"

  # Self-aware: if this is the update script itself, install as JYupdate
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

# Create a global shortcut 'JY' to 'JYhelp'
if [ -f "/usr/local/bin/JYhelp" ]; then
  sudo ln -sf /usr/local/bin/JYhelp /usr/local/bin/JY
  echo "   → Created shortcut 'JY' to 'JYhelp'"
fi

# Print summary of installed JY commands
echo "[*] Installed JY commands:"
ls /usr/local/bin | grep '^JY' | sort

echo "[*] All scripts updated successfully! You can now run them anywhere using JY<commandname>."
echo "[*] Tip: Run 'JY' to see the help menu."
