#!/usr/bin/env bash
# jyhelp — Display available jy commands with descriptions
# Also optionally generates README.md with command info

set -euo pipefail

BIN_DIR="/usr/local/bin"
SCRIPTS_DIR="$HOME/Scripts"
README="$SCRIPTS_DIR/README.md"

# Function to get description from a script
get_desc() {
    local file="$1"
    # Match the first line starting with "# DESC:"
    local desc
    desc=$(grep -m1 "^# *DESC:" "$file" | sed 's/^# *DESC: *//')
    echo "${desc:-No description available}"
}

echo "[*] Available jy commands:"

# Iterate over all jy commands in /usr/local/bin
for cmd_path in "$BIN_DIR"/jy*; do
    [ -f "$cmd_path" ] || continue
    cmd_name="$(basename "$cmd_path")"
    # Skip jyhelp itself
    [ "$cmd_name" == "jyhelp" ] && continue

    # Find corresponding script in Scripts folder
    base_name="${cmd_name#jy}"
    # Check for .sh or .py
    if [ -f "$SCRIPTS_DIR/$base_name.sh" ]; then
        desc=$(get_desc "$SCRIPTS_DIR/$base_name.sh")
    elif [ -f "$SCRIPTS_DIR/$base_name.py" ]; then
        desc=$(get_desc "$SCRIPTS_DIR/$base_name.py")
    else
        desc="No source file found"
    fi

    printf "  %-15s - %s\n" "$cmd_name" "$desc"
done
