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
USERNAME="Supore123"

# Colors
CMATRIX_COLORS=("green" "red" "blue" "white" "yellow" "cyan")
ANSI_COLORS=("\033[1;32m" "\033[1;31m" "\033[1;34m" "\033[1;37m" "\033[1;33m" "\033[1;36m" "\033[1;35m")
RESET="\033[0m"

RAND_INDEX=$((RANDOM % 7))
SELECTED_COLOR="${CMATRIX_COLORS[$RAND_INDEX]}"
SELECTED_ANSI="${ANSI_COLORS[$RAND_INDEX]}"
