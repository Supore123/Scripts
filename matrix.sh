#!/usr/bin/env bash
# DESC: Randomized Matrix boot sequence with ASCII art username greeting
# TAG: matrix, boot, terminal, greeting, ascii
# EXAMPLE: jymatrix

set -euo pipefail

# Ensure the script only runs if a terminal is attached
if [ ! -t 0 ] && [ ! -t 1 ]; then
    exit 0
fi

# Give the terminal a split second to figure out its window size
sleep 0.1

USERNAME="Supore123"

