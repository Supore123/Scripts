#!/usr/bin/env bash
# DESC: Set desktop notifications for reminders
# TAG: remind, alarm, schedule, notification
# EXAMPLE: remind 10 "Take a break"
# EXAMPLE: remind 1 "Water the plants"

MINUTES="$1"
MESSAGE="${*:2}"

if [[ -z "$MINUTES" || -z "$MESSAGE" ]]; then
  echo "Usage: $0 <minutes> <message>"
  exit 1
fi

echo "⏳ Reminder set for $MINUTES minute(s): \"$MESSAGE\""
(sleep $((MINUTES * 60)); notify-send "⏰ Reminder" "$MESSAGE") &

