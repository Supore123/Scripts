#!/usr/bin/env bash
# DESC: Toggle Proton VPN and manage Firefox Private tabs
# TAG: vpn, network, privacy, proton, firefox
# EXAMPLE: jyvpn

set -euo pipefail

URL_CACHE="$HOME/.chrome_bookmarks"
FIREFOX_PROFILE="$HOME/snap/firefox/common/.mozilla/firefox/zcmvniy2.jyvpn"
VPN_PASSWORD="password"

log() { echo -e "\033[1;32m[*]\033[0m $*"; }

kill_gui() {
    if pgrep -f "protonvpn-app|protonvpn-gui" >/dev/null; then
        log "ProtonVPN GUI detected. Killing process..."
        pkill -f "protonvpn-app|protonvpn-gui" || true
        sleep 1
    fi
}

manage_firefox() {
    local action=$1

    if [[ "$action" == "open" ]]; then
        log "Launching Firefox Private..."
        if [[ -s "$URL_CACHE" ]]; then
            mapfile -t sites < <(grep -v '^#' "$URL_CACHE" | grep -v '^$')
        else
            sites=("about:blank")
        fi

        # Open first URL in private window
        firefox --profile "$FIREFOX_PROFILE" --private-window "${sites[0]}" >/dev/null 2>&1 &
        disown

        # Open remaining URLs as new tabs in the same private window
        if [[ ${#sites[@]} -gt 1 ]]; then
            sleep 2
            for url in "${sites[@]:1}"; do
                firefox --profile "$FIREFOX_PROFILE" --new-tab "$url" >/dev/null 2>&1 &
                disown
            done
        fi
        log "Firefox launched."

    elif [[ "$action" == "close" ]]; then
        log "Closing VPN Firefox session..."
        pkill -f "firefox.*zcmvniy2.jyvpn" 2>/dev/null || true
        log "Firefox closed."
    fi
}

if ! command -v protonvpn >/dev/null; then
    echo "Error: protonvpn command not found."
    exit 1
fi

kill_gui

if ip link show | grep -qE "proton0|tun0"; then
    log "VPN active. Disconnecting..."
    manage_firefox "close"
    protonvpn disconnect >/dev/null
    log "Disconnected."
else
    password=$(zenity --password --title="jyvpn" --text="Enter password to connect:") || { log "Aborted."; exit 0; }
    if [[ "$password" != "$VPN_PASSWORD" ]]; then
        zenity --error --title="jyvpn" --text="Incorrect password."
        log "Wrong password. Aborted."
        exit 1
    fi
    log "VPN inactive. Connecting..."
    protonvpn connect >/dev/null
    log "Connected."
    manage_firefox "open"
fi
