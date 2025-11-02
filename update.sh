#!/usr/bin/env bash
# DESC: Copy all scripts in this folder to /usr/local/bin as jy-prefixed commands
#       Handles both .sh and .py scripts
#       Removes old commands not present in the Scripts folder
#       Also creates a global 'jy' command that runs jyhelp

set -euo pipefail

SCRIPTS_DIR="$HOME/Scripts"

echo "[*] Updating global jy commands from $SCRIPTS_DIR..."

# ---------------------------
# Step 1: Install/update scripts (.sh and .py)
# ---------------------------
shopt -s nullglob
for script in "$SCRIPTS_DIR"/*.{sh,py}; do
  [ -f "$script" ] || continue

  # Extract base name without extension
  base_name="$(basename "$script")"
  ext="${base_name##*.}"        # sh or py
  base_name="${base_name%.*}"   # remove extension

  # Self-aware: if this is the update script itself, install as jyupdate
  if [ "$base_name" == "$(basename "$0" .sh)" ] || [ "$base_name" == "$(basename "$0" .py)" ]; then
    name="jyupdate"
  else
    name="jy${base_name}"
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
shopt -u nullglob

# ---------------------------
# Step 2: Cleanup old commands
# ---------------------------
echo "[*] Removing old jy commands not present in $SCRIPTS_DIR..."
for installed in /usr/local/bin/jy*; do
  [ -f "$installed" ] || continue

  installed_name="$(basename "$installed")"       # e.g., jyairpods
  cmd_name="${installed_name#jy}"                 # remove jy prefix

  # Skip jyupdate and jyhelp
  if [[ "$installed_name" == "jyupdate" || "$installed_name" == "jyhelp" || "$installed_name" == "jy" ]]; then
    continue
  fi

  # If the corresponding script does not exist in Scripts folder (.sh or .py), remove it
  if [ ! -f "$SCRIPTS_DIR/$cmd_name.sh" ] && [ ! -f "$SCRIPTS_DIR/$cmd_name.py" ]; then
    echo "   → Removing $installed_name (no source script found)"
    sudo rm "$installed"
  fi
done

# ---------------------------
# Step 3: Create 'jy' shortcut to jyhelp
# ---------------------------
if [ -f "/usr/local/bin/jyhelp" ]; then
  sudo ln -sf /usr/local/bin/jyhelp /usr/local/bin/jy
  echo "   → Created shortcut 'jy' to 'jyhelp'"
fi

# ---------------------------
# Step 4: Summary
# ---------------------------
echo "[*] Installed jy commands:"
ls /usr/local/bin | grep '^jy' | sort

echo "[*] All scripts updated successfully! You can now run them anywhere using jy<commandname>."
echo "[*] Tip: Run 'jy' to see the help menu."
