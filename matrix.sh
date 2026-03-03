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

# Run the matrix effect for 1.25 seconds
if command -v cmatrix >/dev/null 2>&1; then
    timeout --foreground 1.25 cmatrix -b -u 2 -C "$SELECTED_COLOR" 2>/dev/null || true
    clear
fi

# ==========================================
# THE ULTRA-FAST HACKER TRANSITION
# ==========================================

sleep 0.05
echo -e "${SELECTED_ANSI}Initiating root override sequence...${RESET}"
sleep 0.04
echo -e "${SELECTED_ANSI}Routing connection through proxy nodes [7 hops]...${RESET}"
sleep 0.05
echo -e "${SELECTED_ANSI}Bypassing external firewalls...${RESET}"
sleep 0.03
echo -e "${SELECTED_ANSI}Injecting payload into mainframe architecture...${RESET}"
sleep 0.06
echo -e "${SELECTED_ANSI}Extracting encrypted hash tables...${RESET}"
sleep 0.04
echo -e "${SELECTED_ANSI}Cracking 256-bit AES encryption...${RESET}"
sleep 0.05
echo -e "${SELECTED_ANSI}Decrypting secure token...${RESET}"
sleep 0.03
echo -e "${SELECTED_ANSI}Spoofing network MAC address...${RESET}"
sleep 0.04
echo -e "${SELECTED_ANSI}Disabling automated security daemons...${RESET}"
sleep 0.06
echo -e "${SELECTED_ANSI}Verifying cryptographic signatures...${RESET}"
sleep 0.05
echo -e "${SELECTED_ANSI}Establishing zero-trace encrypted tunnel...${RESET}"
sleep 0.06
echo -e "${SELECTED_ANSI}Authenticating user identity...${RESET}"
sleep 0.04

# The dynamic loading bar (cut in half to 0.025s per tick)
echo -n -e "${SELECTED_ANSI}Finalizing system breach: ["
for i in {1..25}; do
    echo -n "█"
    sleep 0.025
done
echo -e "] 100%${RESET}"
sleep 0.25

echo "" # Adds a blank line for spacing before the logo

# ==========================================
# FINAL REVEAL (No screen clear!)
# ==========================================

# Print the matching localized welcome message
echo -e "${SELECTED_ANSI}"

if command -v figlet >/dev/null 2>&1; then
    figlet "$USERNAME"
else
    echo "=== $USERNAME ==="
fi

echo -e "\nACCESS GRANTED. Welcome to the mainframe.${RESET}\n"
