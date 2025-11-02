#!/usr/bin/env bash
# DESC: List all installed JY commands with their descriptions

set -euo pipefail

BIN_DIR="/usr/local/bin"

echo -e "\n🧰 Available JY Commands:\n"

# Find all JY-prefixed scripts
for cmd in "$BIN_DIR"/JY*; do
  [ -x "$cmd" ] || continue
  name="$(basename "$cmd")"

  # Try to extract description from the source file in ~/Scripts
  # or directly from the installed script if accessible
  desc=$(grep -m1 '^# DESC:' "$cmd" 2>/dev/null | cut -d':' -f2- | xargs)

  if [ -z "$desc" ]; then
    desc="(No description available)"
  fi

  printf "%-20s → %s\n" "$name" "$desc"
done

echo -e "\nUse any of the commands above directly (e.g. 'JYairpods').\n"
