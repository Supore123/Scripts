#!/usr/bin/env bash
# DESC: Randomized Matrix boot with original logs and cinematic decryption
# TAG: matrix, boot, terminal, greeting, ascii

set -euo pipefail

# ==========================================
# CONFIGURATION / TIMING CONSTANTS
# ==========================================
# Adjust these for different hardware speeds
DELAY_INITIAL_BUFFER=0.01    # Initial pause before script starts
DELAY_MATRIX_DURATION=0.4    # Total time (seconds) cmatrix runs
DELAY_LOG_LINE=0.01          # Speed of individual hack-log lines
DELAY_LOG_POST_AUTH=0.1      # Brief pause before the progress bar
DELAY_PROGRESS_STEP=0.01     # Speed of the █ characters in the bar
DELAY_POST_BAR=0.1           # Pause after bar hits 100%
DELAY_SNEAKERS_PAUSE=0.05     # How long the "scrambled" text sits before reveal
DELAY_REVEAL_FIGLET=0.00005  # Speed of the ASCII name reveal
DELAY_REVEAL_WELCOME=0.01    # Speed of the final "Access Granted" text

# ==========================================
# CORE LOGIC
# ==========================================

# Ensure the script only runs if a terminal is attached
if [ ! -t 0 ] && [ ! -t 1 ]; then
    exit 0
fi

sneakers_effect() {
    local input="$1"
    local color="$2"
    local speed="$3" 
    local chars="!@#$%^&*()_+{}:<>?=-/\[]{}|;:,."
    
    IFS=$'\n' read -rd '' -a lines <<< "$input" || true

    # 1. Initial Scramble
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
    sleep "$DELAY_SNEAKERS_PAUSE"

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
sleep "$DELAY_INITIAL_BUFFER"
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
    timeout --foreground "$DELAY_MATRIX_DURATION" cmatrix -b -u 2 -C "$SELECTED_COLOR" 2>/dev/null || true
fi

# ==========================================
# THE HACKER TRANSITION (Original Logs)
# ==========================================
echo -e "${SELECTED_ANSI}Initiating root override sequence...${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}Routing connection through proxy nodes [7 hops]...${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}Bypassing external firewalls...${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}Injecting payload into mainframe architecture...${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}Extracting encrypted hash tables...${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}Cracking 256-bit AES encryption...${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}Decrypting secure token...${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}Spoofing network MAC address...${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}Disabling automated security daemons...${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}Verifying cryptographic signatures...${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}Establishing zero-trace encrypted tunnel...${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}Authenticating user identity...${RESET}"
sleep "$DELAY_LOG_POST_AUTH"

# The dynamic loading bar
echo -n -e "${SELECTED_ANSI}Finalizing system breach: ["
for i in {1..25}; do
    echo -n "█"
    sleep "$DELAY_PROGRESS_STEP"
done
echo -e "] 100%${RESET}"
sleep "$DELAY_POST_BAR"
echo "" 

# ==========================================
# FINAL REVEAL (Cinematic Decrypt)
# ==========================================

if command -v figlet >/dev/null 2>&1; then
    USER_ASCII=$(figlet "$USERNAME")
else
    USER_ASCII="=== $USERNAME ==="
fi

sneakers_effect "$USER_ASCII" "$SELECTED_ANSI" "$DELAY_REVEAL_FIGLET"
sneakers_effect "ACCESS GRANTED. Welcome back $USERNAME" "$SELECTED_ANSI" "$DELAY_REVEAL_WELCOME"

echo ""
