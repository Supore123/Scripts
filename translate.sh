#!/usr/bin/env bash
# DESC: Translate text to another language using Google Translate API
# TAG: translate, language, text, convert
# EXAMPLE: translate "good morning" fr
# EXAMPLE: translate "how are you" es

TEXT="$1"
TARGET="$2"

if [[ -z "$TEXT" || -z "$TARGET" ]]; then
  echo "Usage: $0 <text> <target_lang>"
  exit 1
fi

RESULT=$(curl -s "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=$TARGET&dt=t&q=$(echo $TEXT | sed 's/ /%20/g')" | jq -r '.[0][0][0]')
echo "🌐 Translation: $RESULT"

