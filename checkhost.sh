#!/usr/bin/env bash
# DESC: Check if a host (domain or IP) is reachable (ping)
# TAG: network, ping, host, server, online, status, check, down
# EXAMPLE: checkhost google.com
# EXAMPLE: checkhost 1.1.1.1

HOST="$1"

if [[ -z "$HOST" ]]; then
    echo "Usage: $0 <host_or_ip>"
    exit 1
fi

# -c 3 = Send 3 packets
# -W 2 = Wait max 2 seconds for a reply
if ping -c 3 -W 2 "$HOST" &> /dev/null; then
    echo "✅ $HOST is reachable."
else
    echo "❌ $HOST is unreachable."
fi
