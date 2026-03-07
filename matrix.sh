#!/usr/bin/env bash
# DESC: Randomized Matrix boot with original logs and cinematic decryption
# TAG: matrix, boot, terminal, greeting, ascii

set -euo pipefail

# Ensure the script only runs if a terminal is attached
if [ ! -t 0 ] && [ ! -t 1 ]; then
    exit 0
fi
# ==========================================
# CINEMATIC DECRYPTION FUNCTION
# ==========================================
sneakers_effect() {
    local input="$1"
    local color="$2"
    local speed="$3" 
    local chars="!@#$%^&*()_+{}:<>?=-/\[]{}|;:,."
    
    IFS=$'\n' read -rd '' -a lines <<< "$input" || true

    # 1. Initial Scramble (Briefly show gibberish)
    echo -ne "${color}"
    for line in "${lines[@]}"; do
        for ((i=0; i<${#line}; i++)); do
            char="${line:$i:1}"
            [[ "$char" == " " ]] && echo -n " " || echo -n "${chars:$((RANDOM % ${#chars})):1}"
        done
        echo "" 
    done

    # 2. Pause slightly so the scramble is visible
    local num_lines=${#lines[@]}
    echo -ne "\033[${num_lines}A" 
    sleep 0.2

    # 3. Reveal Phase
    for line in "${lines[@]}"; do
        for ((i=0; i<${#line}; i++)); do
            echo -n "${line:$i:1}"
            sleep "$speed" 
        done
        echo "" 
    done
    echo -ne "${RESET}"
}
# Terminal setup
sleep 0.1
USERNAME=$(whoami)

# Colors
CMATRIX_COLORS=("green" "red" "blue" "white" "yellow" "cyan")
ANSI_COLORS=("\033[1;32m" "\033[1;31m" "\033[1;34m" "\033[1;37m" "\033[1;33m" "\033[1;36m" "\033[1;35m")
RESET="\033[0m"

RAND_INDEX=$((RANDOM % 6))
SELECTED_COLOR="${CMATRIX_COLORS[$RAND_INDEX]}"
SELECTED_ANSI="${ANSI_COLORS[$RAND_INDEX]}"
# 1. Matrix Effect
if command -v cmatrix >/dev/null 2>&1; then
    timeout --foreground 1.25 cmatrix -b -u 2 -C "$SELECTED_COLOR" 2>/dev/null || true
fi
# ==========================================
# THE HACKER TRANSITION (Original Logs)
# ==========================================
sleep 0.05
echo -e "${SELECTED_ANSI}Initiating root override sequence...${RESET}"
sleep 0.1
echo -e "${SELECTED_ANSI}Routing connection through proxy nodes [7 hops]...${RESET}"
sleep 0.1
echo -e "${SELECTED_ANSI}Bypassing external firewalls...${RESET}"
sleep 0.1
echo -e "${SELECTED_ANSI}Injecting payload into mainframe architecture...${RESET}"
sleep 0.1
echo -e "${SELECTED_ANSI}Extracting encrypted hash tables...${RESET}"
sleep 0.1
echo -e "${SELECTED_ANSI}Cracking 256-bit AES encryption...${RESET}"
sleep 0.1
echo -e "${SELECTED_ANSI}Decrypting secure token...${RESET}"
sleep 0.1
echo -e "${SELECTED_ANSI}Spoofing network MAC address...${RESET}"
sleep 0.1
echo -e "${SELECTED_ANSI}Disabling automated security daemons...${RESET}"
sleep 0.1
echo -e "${SELECTED_ANSI}Verifying cryptographic signatures...${RESET}"
sleep 0.1
echo -e "${SELECTED_ANSI}Establishing zero-trace encrypted tunnel...${RESET}"
sleep 0.1
echo -e "${SELECTED_ANSI}Authenticating user identity...${RESET}"
sleep 0.2

# The dynamic loading bar
echo -n -e "${SELECTED_ANSI}Finalizing system breach: ["
for i in {1..25}; do
    echo -n "█"
    sleep 0.02
done
echo -e "] 100%${RESET}"
sleep 0.3
echo "" 
# ==========================================
# FINAL REVEAL (Cinematic Decrypt)
# ==========================================

if command -v figlet >/dev/null 2>&1; then
    USER_ASCII=$(figlet "$USERNAME")
else
    USER_ASCII="=== $USERNAME ==="
fi

# Adjusted speeds: 0.0001 for Figlet, 0.002 for the message
sneakers_effect "$USER_ASCII" "$SELECTED_ANSI" 0.0001
sneakers_effect "ACCESS GRANTED. Welcome back $USERNAME" "$SELECTED_ANSI" 0.002

echo ""
