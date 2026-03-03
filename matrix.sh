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

# Define lists of cmatrix colors
CMATRIX_COLORS=("green" "red" "blue" "white" "yellow" "cyan" "magenta")
ANSI_COLORS=(
    "\033[1;32m" # green
    "\033[1;31m" # red
    "\033[1;34m" # blue
    "\033[1;37m" # white
    "\033[1;33m" # yellow
    "\033[1;36m" # cyan
    "\033[1;35m" # magenta
)
RESET="\033[0m"

RAND_INDEX=$((RANDOM % 7))
SELECTED_COLOR="${CMATRIX_COLORS[$RAND_INDEX]}"
SELECTED_ANSI="${ANSI_COLORS[$RAND_INDEX]}"

