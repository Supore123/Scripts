#!/usr/bin/env bash
# DESC: Connect, disconnect, and show AirPods battery status
# TAG: bluetooth, audio, airpods, headphones, wireless
# ARG: [MAC_ADDRESS] - Bluetooth MAC address (optional, uses default)
# EXAMPLE: jyairpods
# EXAMPLE: jyairpods 0C:53:B7:8E:4A:62

set -euo pipefail

MAC_DEFAULT="0C:53:B7:8E:4A:62"
MAC="${1:-$MAC_DEFAULT}"
MAC="$(echo "$MAC" | tr '[:lower:]' '[:upper:]')"

log() { echo -e "\033[1;32m[*]\033[0m $*"; }

if ! command -v bluetoothctl >/dev/null; then
  echo "Error: bluetoothctl not found. Install bluez and retry."
  exit 1
fi

log "Powering on Bluetooth..."
bluetoothctl power on >/dev/null

# Make sure device is paired & trusted
if ! bluetoothctl info "$MAC" | grep -q "Paired: yes"; then
  log "Pairing and trusting $MAC..."
  bluetoothctl pair "$MAC" || true
  bluetoothctl trust "$MAC" || true
else
  log "Device already paired/trusted."
fi

# Check if device is already connected
if bluetoothctl info "$MAC" | grep -q "Connected: yes"; then
  log "AirPods are already connected. Disconnecting..."
  bluetoothctl disconnect "$MAC" >/dev/null && log "Disconnected successfully."
  exit 0
fi

# Try connecting
log "Connecting to AirPods ($MAC)..."
connected=false
for i in {1..5}; do
  if bluetoothctl connect "$MAC" 2>&1 | grep -q "Connection successful"; then
    connected=true
    break
  fi
  sleep 2
done

if [ "$connected" = false ]; then
  log "Failed to connect to $MAC after 5 attempts."
  exit 1
fi

log "Connected successfully!"

# Show battery
show_battery() {
  info=$(bluetoothctl info "$MAC")
  left=$(echo "$info" | grep "Battery Percentage (L)" | awk '{print $4}' || true)
  right=$(echo "$info" | grep "Battery Percentage (R)" | awk '{print $4}' || true)
  case_battery=$(echo "$info" | grep "Battery Percentage (Case)" | awk '{print $4}' || true)

  if [ -n "$left" ] || [ -n "$right" ] || [ -n "$case_battery" ]; then
    [ -n "$left" ] && log "Left AirPod: $left%"
    [ -n "$right" ] && log "Right AirPod: $right%"
    [ -n "$case_battery" ] && log "Case: $case_battery%"
  else
    log "Battery info not available."
  fi
}

show_battery

# Set audio sink
if command -v pactl >/dev/null; then
  mac_lower=$(echo "$MAC" | tr ':' '_' | tr '[:upper:]' '[:lower:]')
  sink=$(pactl list short sinks | grep "$mac_lower" | awk '{print $2}' | head -n1 || true)
  if [ -n "$sink" ]; then
    log "Setting $sink as default audio output."
    pactl set-default-sink "$sink"
    for input in $(pactl list short sink-inputs | awk '{print $1}'); do
      pactl move-sink-input "$input" "$sink"
    done
  fi
fi

log "Done!"
