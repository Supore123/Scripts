#!/usr/bin/env bash
# DESC: Toggle Proton VPN connection (Force kills GUI to free CLI)
# TAG: vpn, network, privacy, proton
# ARG: None - toggles connection
# EXAMPLE: jyvpn

set -euo pipefail

log() { echo -e "\033[1;32m[*]\033[0m $*"; }

# Function to kill the GUI process if it is running
kill_gui() {
    # Check for common ProtonVPN GUI process names
    # 'protonvpn-app' is the standard for the modern Linux app
    if pgrep -f "protonvpn-app|protonvpn-gui" >/dev/null; then
        log "ProtonVPN GUI detected. Killing process to free up CLI..."
        # pkill -f matches against the full command line
        pkill -f "protonvpn-app|protonvpn-gui" || true
        
        # Wait a brief moment to ensure the process releases the lock
        sleep 1
    fi
}

if ! command -v protonvpn >/dev/null; then
  echo "Error: protonvpn command not found."
  exit 1
fi

# Kill the GUI before checking status or toggling
kill_gui

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
