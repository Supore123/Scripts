#!/usr/bin/env bash
# JYhelp — Display available JY commands with descriptions
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

echo "[*] Available JY commands:"

# Iterate over all JY commands in /usr/local/bin
for cmd_path in "$BIN_DIR"/JY*; do
    [ -f "$cmd_path" ] || continue
    cmd_name="$(basename "$cmd_path")"
    # Skip JYhelp itself
    [ "$cmd_name" == "JYhelp" ] && continue

    # Find corresponding script in Scripts folder
    base_name="${cmd_name#JY}"
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

# Optionally update README.md automatically
update_readme() {
    echo "# JY Scripts" > "$README"
    echo "" >> "$README"
    echo "## Available Commands" >> "$README"
    echo "" >> "$README"

    for cmd_path in "$BIN_DIR"/JY*; do
        [ -f "$cmd_path" ] || continue
        cmd_name="$(basename "$cmd_path")"
        [ "$cmd_name" == "JYhelp" ] && continue
        base_name="${cmd_name#JY}"
        if [ -f "$SCRIPTS_DIR/$base_name.sh" ]; then
            desc=$(get_desc "$SCRIPTS_DIR/$base_name.sh")
        elif [ -f "$SCRIPTS_DIR/$base_name.py" ]; then
            desc=$(get_desc "$SCRIPTS_DIR/$base_name.py")
        else
            desc="No source file found"
        fi
        echo "### $cmd_name" >> "$README"
        echo "" >> "$README"
        echo "$desc" >> "$README"
        echo "" >> "$README"
    done

    echo "[*] README.md updated at $README"
}

# Uncomment the following line if you want README auto-update each time help is run
# update_readme
