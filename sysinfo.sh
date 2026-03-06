#!/usr/bin/env bash
# DESC: Display detailed high-precision system info (CPU, RAM, Disk, GPU, Network, Uptime, Battery)

set -euo pipefail

# Colors
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
CYAN="\033[1;36m"
RESET="\033[0m"

echo -e "${CYAN}🖥️  System Information (High Precision)${RESET}"
echo "----------------------------------------"

# Hostname & Uptime
echo -e "${GREEN}Hostname:${RESET} $(hostname)"
echo -e "${GREEN}Uptime:${RESET} $(uptime -p)"

# CPU Info
CPU_CORES=$(nproc)
CPU_LOAD=$(uptime | awk -F'load average:' '{ print $2 }' | xargs)
echo -e "${GREEN}CPU Cores:${RESET} $CPU_CORES"
echo -e "${GREEN}CPU Load:${RESET} $CPU_LOAD"

# Memory Info (High Precision)
# Pulling in KB and dividing by 1048576 (1024^2) for true GB decimals
MEM_DATA=$(free -k | awk '/Mem:/ {
    total = $2 / 1048576;
    used = $3 / 1048576;
    free = $4 / 1048576;
    printf "%.2fG used / %.2fG total (%.2fG free)", used, total, free
}')
echo -e "${GREEN}RAM:${RESET} $MEM_DATA"

# Disk Info (High Precision)
# Pulling in KB (-k) to avoid the rounding inherent in df -h or df -BG
DISK=$(df -k / | awk 'NR==2 {
    total = $2 / 1048576;
    used = $3 / 1048576;
    free = $4 / 1048576;
    usage = $5;
    printf "%.2fG used / %.2fG total | %.2fG left (%s used)", used, total, free, usage
}')
echo -e "${GREEN}Disk (root):${RESET} $DISK"

# GPU Info (High Precision)
if command -v nvidia-smi >/dev/null 2>&1; then
    # Query raw MiB values
    GPU_DATA=$(nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader,nounits)
    
    GPU_NAME=$(echo "$GPU_DATA" | cut -d',' -f1)
    GPU_USED_MIB=$(echo "$GPU_DATA" | cut -d',' -f2)
    GPU_TOTAL_MIB=$(echo "$GPU_DATA" | cut -d',' -f3)
    
    # Convert MiB to GB with 2 decimal places
    GPU_USED_GB=$(awk "BEGIN {printf \"%.2f\", $GPU_USED_MIB/1024}")
    GPU_TOTAL_GB=$(awk "BEGIN {printf \"%.2f\", $GPU_TOTAL_MIB/1024}")
    
    echo -e "${GREEN}GPU:${RESET} $GPU_NAME ($GPU_USED_GB GB / $GPU_TOTAL_GB GB used)"
fi

# Battery Info via upower
if command -v upower >/dev/null 2>&1; then
    BATTERY=$(upower -e | grep 'BAT' | head -n 1 || true)
    if [ -n "$BATTERY" ]; then
        BAT_INFO=$(upower -i "$BATTERY")
        PERCENT=$(echo "$BAT_INFO" | awk '/percentage:/ {print $2}' | tr -d '%')
        STATUS=$(echo "$BAT_INFO" | awk '/state:/ {print $2}')
        TIME=$(echo "$BAT_INFO" | awk '/time to full:/ {print $4 " " $5} /time to empty:/ {print $4 " " $5}')
        POWER=$(echo "$BAT_INFO" | awk '/energy-rate:/ {print $2 " W"}')
        
        # Progress bar
        BAR_LENGTH=20
        PERCENT_VAL=${PERCENT:-0}
        FILLED=$(( PERCENT_VAL * BAR_LENGTH / 100 ))
        EMPTY=$(( BAR_LENGTH - FILLED ))
        
        if [ "$PERCENT_VAL" -ge 50 ]; then
            BAR_COLOR=$GREEN
        elif [ "$PERCENT_VAL" -ge 20 ]; then
            BAR_COLOR=$YELLOW
        else
            BAR_COLOR=$RED
        fi
        
        # Creating bar with compatibility check for seq
        PROGRESS_BAR="${BAR_COLOR}$(printf '█%.0s' $(seq 1 $FILLED 2>/dev/null || echo ""))$(printf '░%.0s' $(seq 1 $EMPTY 2>/dev/null || echo ""))${RESET}"
        
        echo -e "${GREEN}Battery:${RESET} $PERCENT% ($STATUS, $POWER, $TIME) $PROGRESS_BAR"
    else
        echo -e "${GREEN}Battery:${RESET} No battery found"
    fi
else
    echo -e "${YELLOW}Battery:${RESET} upower not installed"
fi

# Network Info
IP_LOCAL=$(hostname -I | awk '{print $1}')
IP_PUBLIC=$(curl -s --max-time 2 ifconfig.me || echo "N/A")
echo -e "${GREEN}Local IP:${RESET} $IP_LOCAL"
echo -e "${GREEN}Public IP:${RESET} $IP_PUBLIC"

echo "----------------------------------------"
echo -e "${CYAN}✅ Done${RESET}"
