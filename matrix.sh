#!/usr/bin/env bash
# DESC: Cross-platform System Diagnostic Boot with Synchronized Colors
# TAG: matrix, boot, terminal, hardware, unix

set -euo pipefail

# ==========================================
# CONFIGURATION / TIMING CONSTANTS
# ==========================================
DELAY_INITIAL_BUFFER=0.01    
DELAY_MATRIX_DURATION=0.4    
DELAY_LOG_LINE=0.02          
DELAY_LOG_POST_AUTH=0.1      
DELAY_PROGRESS_STEP=0.01     
DELAY_POST_BAR=0.1           
DELAY_SNEAKERS_PAUSE=0.01    
DELAY_REVEAL_FIGLET=0.00005  
DELAY_REVEAL_WELCOME=0.01    

# ==========================================
# SYSTEM DATA GATHERING (Cross-Platform)
# ==========================================
USERNAME=$(whoami)
HOSTNAME=$(hostname)
KERNEL=$(uname -r)

if [ -f /etc/os-release ]; then
    OS_NAME=$(grep '^PRETTY_NAME=' /etc/os-release | cut -d'"' -f2)
else
    OS_NAME=$(uname -s)
fi

IP_ADDR=$(hostname -I | awk '{print $1}')
[ -z "$IP_ADDR" ] && IP_ADDR="127.0.0.1 (Offline)"

MEM_FREE=$(free -h | awk '/^Mem:/ {print $4 "/" $2}')
UPTIME=$(uptime -p | sed 's/up //')

# --- NEW DYNAMIC LOG DATA ---
DISK_USAGE=$(df -h / | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}')
CPU_LOAD=$(top -bn1 | grep "load average" | awk '{print $(NF-2)}' | sed 's/,//')
PROCESS_COUNT=$(ps ax | wc -l | tr -d ' ')
SHELL_PATH=$SHELL

# Battery Check
if [ -d /sys/class/power_supply/BAT0 ]; then
    BATT_STAT=$(cat /sys/class/power_supply/BAT0/capacity 2>/dev/null || echo "N/A")
    BATTERY_STR="[OK] Power Cell Capacity: ${BATT_STAT}%"
else
    BATTERY_STR=""
fi

HOUR=$(date +%H)
if [ "$HOUR" -lt 12 ]; then GREET="Good Morning"; 
elif [ "$HOUR" -lt 18 ]; then GREET="Good Afternoon"; 
else GREET="Good Evening"; fi

# ==========================================
# CORE LOGIC
# ==========================================

if [ ! -t 0 ] && [ ! -t 1 ]; then
    exit 0
fi

if read -t 0.1 -n 1; then
    exit 0
fi

sneakers_effect() {
    local input="$1"
    local color="$2"
    local speed="$3" 
    local chars="!@#$%^&*()_+{}:<>?=-/\[]{}|;:,."
    
    IFS=$'\n' read -rd '' -a lines <<< "$input" || true

    echo -ne "${color}"
    for line in "${lines[@]}"; do
        for ((i=0; i<${#line}; i++)); do
            char="${line:$i:1}"
            [[ "$char" == " " ]] && echo -n " " || echo -n "${chars:$((RANDOM % ${#chars})):1}"
        done
        echo "" 
    done

    local num_lines=${#lines[@]}
    echo -ne "\033[${num_lines}A" 
    sleep "$DELAY_SNEAKERS_PAUSE"

    for line in "${lines[@]}"; do
        for ((i=0; i<${#line}; i++)); do
            echo -n "${line:$i:1}"
            sleep "$speed" 
        done
        echo "" 
    done
    echo -ne "\033[0m"
}

# --- SYNCHRONIZED COLORS ---
# cmatrix supports: green, red, blue, white, yellow, cyan, magenta
CMATRIX_COLORS=("green" "red" "blue" "white" "yellow" "cyan" "magenta")
ANSI_COLORS=("\033[1;32m" "\033[1;31m" "\033[1;34m" "\033[1;37m" "\033[1;33m" "\033[1;36m" "\033[1;35m")
RESET="\033[0m"

# Use the same index for both arrays
RAND_INDEX=$((RANDOM % ${#CMATRIX_COLORS[@]}))
SELECTED_COLOR="${CMATRIX_COLORS[$RAND_INDEX]}"
SELECTED_ANSI="${ANSI_COLORS[$RAND_INDEX]}"

# 1. Matrix Effect
if command -v cmatrix >/dev/null 2>&1; then
    timeout --foreground "$DELAY_MATRIX_DURATION" cmatrix -b -u 2 -C "$SELECTED_COLOR" 2>/dev/null || true
fi

# ==========================================
# REAL SYSTEM LOGS (Now with dynamic hardware data)
# ==========================================
sleep "$DELAY_INITIAL_BUFFER"
echo -e "${SELECTED_ANSI}[OK] Host: $HOSTNAME | OS: $OS_NAME${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}[OK] Kernel Release: $KERNEL${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}[OK] IPv4 Address: $IP_ADDR${RESET}"
sleep "$DELAY_LOG_LINE"

if [ -n "$BATTERY_STR" ]; then
    echo -e "${SELECTED_ANSI}$BATTERY_STR${RESET}"
    sleep "$DELAY_LOG_LINE"
fi

echo -e "${SELECTED_ANSI}[OK] Memory: $MEM_FREE | Load: $CPU_LOAD${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}[OK] Root Filesystem: $DISK_USAGE used${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}[OK] Active Task Count: $PROCESS_COUNT tasks${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}[OK] Shell Environment: $SHELL_PATH${RESET}"
sleep "$DELAY_LOG_LINE"
echo -e "${SELECTED_ANSI}[OK] Uptime: $UPTIME${RESET}"
sleep "$DELAY_LOG_POST_AUTH"

# Loading bar
echo -n -e "${SELECTED_ANSI}Mounting Filesystems: ["
for i in {1..25}; do
    echo -n "█"
    sleep "$DELAY_PROGRESS_STEP"
done
echo -e "] 100%${RESET}"
sleep "$DELAY_POST_BAR"
echo "" 

# ==========================================
# FINAL REVEAL
# ==========================================
if command -v figlet >/dev/null 2>&1; then
    USER_ASCII=$(figlet "$USERNAME")
else
    USER_ASCII="=== $USERNAME ==="
fi

sneakers_effect "$USER_ASCII" "$SELECTED_ANSI" "$DELAY_REVEAL_FIGLET"
sneakers_effect "ACCESS GRANTED. $GREET, $USERNAME" "$SELECTED_ANSI" "$DELAY_REVEAL_WELCOME"

echo ""
