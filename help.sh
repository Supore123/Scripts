#!/usr/bin/env bash
# DESC: Display all available jy commands with descriptions
# TAG: help, commands, documentation
# ARG: None - lists all commands
# EXAMPLE: jyhelp

set -euo pipefail

BIN_DIR="/usr/local/bin"
SCRIPTS_DIR="$HOME/Scripts"

get_desc() {
    local file="$1"
    local desc
    desc=$(grep -m1 "^# *DESC:" "$file" 2>/dev/null | sed 's/^# *DESC: *//')
    echo "${desc:-No description available}"
}

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║     📚 Available jy Commands          ║"
echo "╚═══════════════════════════════════════╝"
echo ""

for cmd_path in "$BIN_DIR"/jy*; do
    [ -f "$cmd_path" ] || continue
    cmd_name="$(basename "$cmd_path")"

    # Skip jyhelp itself
    [ "$cmd_name" == "jyhelp" ] && continue

    base_name="${cmd_name#jy}"

    if [ -f "$SCRIPTS_DIR/$base_name.sh" ]; then
        desc=$(get_desc "$SCRIPTS_DIR/$base_name.sh")
    elif [ -f "$SCRIPTS_DIR/$base_name.py" ]; then
        desc=$(get_desc "$SCRIPTS_DIR/$base_name.py")
    else
        desc="No source file found"
    fi

    printf "  • %-15s %s\n" "$cmd_name" "$desc"
done

echo ""
echo "💡 For detailed help: jyhelp <command>"
echo "💬 Or chat with me: jychat"
echo ""
