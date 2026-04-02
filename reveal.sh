#!/usr/bin/env bash
# DESC: A "Sneakers" style text reveal tool for piped input.

set -euo pipefail

# Speed settings (adjust to your taste)
DELAY_SNEAKERS_PAUSE=0.01
DELAY_REVEAL_SPEED=0.001

# If no input is piped in and no arguments given, show usage
if [ -t 0 ] && [ $# -eq 0 ]; then
    echo "Usage: figlet 'Hello' | ./reveal"
    exit 1
fi

# Capture input from pipe or arguments
input=$(cat -)

sneakers_reveal() {
    local content="$1"
    local chars="!@#$%^&*()_+{}:<>?=-/\[]{}|;:,."
    
    # Split input into an array of lines
    IFS=$'\n' read -rd '' -a lines <<< "$content" || true

    # Phase 1: Print "Garbage" characters
    for line in "${lines[@]}"; do
        for ((i=0; i<${#line}; i++)); do
            char="${line:$i:1}"
            if [[ "$char" == " " ]]; then
                echo -n " "
            else
                echo -n "${chars:$((RANDOM % ${#chars})):1}"
            fi
        done
        echo "" 
    done

    # Move cursor back up to the start of the block
    local num_lines=${#lines[@]}
    echo -ne "\033[${num_lines}A" 
    sleep "$DELAY_SNEAKERS_PAUSE"

    # Phase 2: Reveal the actual characters
    for line in "${lines[@]}"; do
        for ((i=0; i<${#line}; i++)); do
            echo -n "${line:$i:1}"
            sleep "$DELAY_REVEAL_SPEED" 
        done
        echo "" 
    done
}

# Run the effect
sneakers_reveal "$input"
