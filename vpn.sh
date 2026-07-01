#!/usr/bin/env bash
# DESC: Toggle Proton VPN, Password Check, and Chrome Incognito with Bookmarks
# TAG: vpn, chrome, security

set -euo pipefail

# --- CONFIGURATION ---
BOOKMARKS="$HOME/.chrome_bookmarks"
# Set your desired script password here
SCRIPT_PASSWORD="password"

# 1. Kill the Proton VPN GUI if it's running
if pgrep -f "protonvpn-app|protonvpn-gui" >/dev/null; then
  pkill -9 -f "protonvpn-app|protonvpn-gui" || true
  sleep 1
fi

# 2. Toggle Logic
if ip link show | grep -qE "proton|tun0|ipv6leak"; then
  # --- DISCONNECTING ---

  pkill -9 -f "chrome-vpn-session" || true
  rm -rf /tmp/chrome-vpn-session

  protonvpn disconnect >/dev/null
else
  # --- PASSWORD CHECK ---
  # Opens a graphical password entry box
  INPUT_PASS=$(zenity --password --title="VPN Access Control" --text="Enter password to enable VPN and Browser:")

  # If the user hits cancel or enters the wrong password
  if [[ "$INPUT_PASS" != "$SCRIPT_PASSWORD" ]]; then
    notify-send "Access Denied" "Incorrect password or action cancelled."
    exit 1
  fi

  if protonvpn connect; then
    # Read the bookmarks into an array
    if [[ -f "$BOOKMARKS" ]]; then
      mapfile -t urls < <(grep -v '^\s*$\|^\s*#' "$BOOKMARKS")
    else
      urls=("about:blank")
    fi

    # Launch Chrome with all URLs as tabs
    google-chrome --incognito --new-window \
      --user-data-dir="/tmp/chrome-vpn-session" \
      --no-first-run \
      --no-default-browser-check \
      --start-maximized \
      --disable-features=AudioServiceOutOfProcess %U \
      "${urls[@]}" >/dev/null 2>&1 &
    disown
  else
    notify-send "VPN" "Failed to connect."
    exit 1
  fi
fi
