#!/usr/bin/env bash
# DESC: Copy all scripts in this folder to /usr/local/bin as JY-prefixed commands
#       Removes old commands not present in the Scripts folder
#       Also creates a global 'JY' command that runs JYhelp

set -euo pipefail

SCRIPTS_DIR="$HOME/Scripts"

echo "[*] Updating global JY commands from $SCRIPTS_DIR..."

# ---------------------------
# Step 1: Install/update scripts
# ---------------------------
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

# ---------------------------
# Step 2: Cleanup old commands
# ---------------------------
echo "[*] Removing old JY commands not present in $SCRIPTS_DIR..."
for installed in /usr/local/bin/JY*; do
  [ -f "$installed" ] || continue

  installed_name="$(basename "$installed")"       # e.g., JYairpods
  cmd_name="${installed_name#JY}"                 # remove JY prefix

  # Skip JYupdate and JYhelp
  if [[ "$installed_name" == "JYupdate" || "$installed_name" == "JYhelp" || "$installed_name" == "JY" ]]; then
    continue
  fi

  # If the corresponding script does not exist in Scripts folder, remove it
  if [ ! -f "$SCRIPTS_DIR/$cmd_name.sh" ]; then
    echo "   → Removing $installed_name (no source script found)"
    sudo rm "$installed"
  fi
done

# ---------------------------
# Step 3: Create 'JY' shortcut to JYhelp
# ---------------------------
if [ -f "/usr/local/bin/JYhelp" ]; then
  sudo ln -sf /usr/local/bin/JYhelp /usr/local/bin/JY
  echo "   → Created shortcut 'JY' to 'JYhelp'"
fi

# ---------------------------
# Step 4: Summary
# ---------------------------
echo "[*] Installed JY commands:"
ls /usr/local/bin | grep '^JY' | sort

echo "[*] All scripts updated successfully! You can now run them anywhere using JY<commandname>."
echo "[*] Tip: Run 'JY' to see the help menu."
