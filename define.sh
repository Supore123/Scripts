#!/usr/bin/env bash
# DESC: Get the definition of an English word
# TAG: define, dictionary, word, meaning, language, learn
# EXAMPLE: define hello
# EXAMPLE: define "cognitive dissonance"

WORD="$1"
if [[ -z "$WORD" ]]; then
    echo "Usage: $0 <word>"
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "❌ Error: jq is not installed. Please install it."
    exit 1
fi

# URL encode
WORD_ENCODED=$(echo "$WORD" | sed 's/ /%20/g')
API_URL="https://api.dictionaryapi.dev/api/v2/entries/en/$WORD_ENCODED"

# Use curl and jq. Use --fail to exit non-zero if 404
RESPONSE=$(curl -s --fail "$API_URL")

if [[ $? -ne 0 ]]; then
    echo "❌ Could not find a definition for '$WORD'."
    exit 1
fi

# Extract the first definition
DEFINITION=$(echo "$RESPONSE" | jq -r '.[0].meanings[0].definitions[0].definition' 2>/dev/null)

if [[ -z "$DEFINITION" || "$DEFINITION" == "null" ]]; then
    echo "❌ Definition format was unreadable. Try another word."
    exit 1
fi

echo "📖 $WORD: $DEFINITION"
