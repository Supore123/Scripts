#!/usr/bin/env bash
# DESC: Show current weather in your city using wttr.in
# TAG: weather, forecast, temperature, sky
# EXAMPLE: weather london
# EXAMPLE: weather

CITY="${1:-London}"
echo "🌦️  Weather for $CITY"
curl -s "wttr.in/$CITY?format=3"

