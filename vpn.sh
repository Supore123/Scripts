#!/usr/bin/env bash
# DESC: Toggle Proton VPN and manage Incognito Chrome tabs
# TAG: vpn, network, privacy, proton, chrome
# ARG: None - toggles connection
# EXAMPLE: jyvpn

set -euo pipefail

log() { echo -e "\033[1;32m[*]\033[0m $*"; }

kill_gui() {
    if pgrep -f "protonvpn-app|protonvpn-gui" >/dev/null; then
        log "ProtonVPN GUI detected. Killing process..."
        pkill -f "protonvpn-app|protonvpn-gui" || true
        sleep 1
    fi
}

# New function to handle Chrome Incognito
manage_chrome() {
    local action=$1
    if [[ "$action" == "open" ]]; then
        log "Launching Chrome Incognito..."
        # Opens a new incognito window and detaches it from the terminal
        google-chrome --incognito "about:blank" >/dev/null 2>&1 &
    elif [[ "$action" == "close" ]]; then
        log "Closing all Incognito tabs..."
        # This kills processes specifically marked with the incognito flag
        pkill -f "google-chrome.*--incognito" || true
    fi
}

if ! command -v protonvpn >/dev/null; then
  echo "Error: protonvpn command not found."
  exit 1
fi

kill_gui

# Check connection status
if ip link show | grep -qE "proton0|tun0"; then
    log "VPN connection detected. Disconnecting..."
    
    # 1. Close Chrome Incognito FIRST for privacy
    manage_chrome "close"
    
    # 2. Disconnect VPN
    protonvpn disconnect >/dev/null
    log "Disconnected."
else
    log "VPN is disconnected. Connecting..."
    
    # 1. Connect VPN
    protonvpn connect >/dev/null
    log "Connected."
    
    # 2. Open Chrome Incognito AFTER connection is secured
    manage_chrome "open"
fi
