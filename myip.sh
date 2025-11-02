#!/usr/bin/env bash
# DESC: Get your public (external) IP address
# TAG: network, ip, public, external, address, wifi, internet
# EXAMPLE: myip

# We use icanhazip.com because it returns only the IP as plain text
IP=$(curl -s icanhazip.com)

if [[ -n "$IP" ]]; then
    echo "🌍 Public IP: $IP"
else
    echo "❌ Could not retrieve public IP. Check internet connection."
    exit 1
fi
