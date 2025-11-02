#!/usr/bin/env bash
# DESC: Display detailed system info (CPU, RAM, Disk, GPU, Network, Uptime)

set -euo pipefail

# Colors
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
CYAN="\033[1;36m"
RESET="\033[0m"

echo -e "${CYAN}🖥️  System Information${RESET}"
echo "----------------------------------------"

# Hostname & Uptime
echo -e "${GREEN}Hostname:${RESET} $(hostname)"
echo -e "${GREEN}Uptime:${RESET} $(uptime -p)"

# CPU Info
CPU_CORES=$(nproc)
CPU_LOAD=$(uptime | awk -F'load average:' '{ print $2 }' | xargs)
echo -e "${GREEN}CPU Cores:${RESET} $CPU_CORES"
echo -e "${GREEN}CPU Load:${RESET} $CPU_LOAD"

# Memory Info
MEM_TOTAL=$(free -h | awk '/Mem:/ {print $2}')
MEM_USED=$(free -h | awk '/Mem:/ {print $3}')
MEM_FREE=$(free -h | awk '/Mem:/ {print $4}')
echo -e "${GREEN}RAM:${RESET} $MEM_USED used / $MEM_TOTAL total ($MEM_FREE free)"

# Disk Info
DISK=$(df -h / | awk 'NR==2 {print $3 " used / " $2 " total (" $5 " used)"}')
echo -e "${GREEN}Disk (root):${RESET} $DISK"

# GPU Info (if NVIDIA)
if command -v nvidia-smi >/dev/null 2>&1; then
    GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader)
    GPU_MEM=$(nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader)
    echo -e "${GREEN}GPU:${RESET} $GPU_NAME ($GPU_MEM MB used)"
fi

# Network Info
IP_LOCAL=$(hostname -I | awk '{print $1}')
IP_PUBLIC=$(curl -s ifconfig.me || echo "N/A")
echo -e "${GREEN}Local IP:${RESET} $IP_LOCAL"
echo -e "${GREEN}Public IP:${RESET} $IP_PUBLIC"

echo "----------------------------------------"
echo -e "${CYAN}✅ Done${RESET}"

