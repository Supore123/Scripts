#!/usr/bin/env bash
# DESC: Toggle Proton VPN connection
# TAG: vpn, network, privacy, proton
# ARG: None - toggles connection
# EXAMPLE: jyvpn

set -euo pipefail

log() { echo -e "\033[1;32m[*]\033[0m $*"; }

if ! command -v protonvpn >/dev/null; then
  echo "Error: protonvpn command not found."
  exit 1
fi

# Check connection status via network interface
# (Standard Proton interfaces are 'proton0' or 'tun0')
if ip link show | grep -qE "proton0|tun0"; then
  log "VPN connection detected. Disconnecting..."
  protonvpn disconnect >/dev/null
  log "Disconnected."
else
  log "VPN is disconnected. Connecting..."
  # Connects to the fastest available server automatically
  protonvpn connect >/dev/null
  log "Connected."
fi
