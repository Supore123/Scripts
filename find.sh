#!/usr/bin/env bash
# DESC: Interactively find a file or directory using fzf (and fd if available)
# TAG: find, file, search, fzf, open, ffind, grep
# EXAMPLE: ffind (opens interactive finder)

if ! command -v fzf &> /dev/null; then
    echo "❌ Error: fzf is not installed."
    exit 1
fi

SEARCH_CMD=""
# Prefer fd (fdfind on debian) if it exists
if command -v fd &> /dev/null; then
    # Find all files/dirs, including hidden
    SEARCH_CMD="fd --type f --type d --hidden --exclude .git"
elif command -v fdfind &> /dev/null; then
    SEARCH_CMD="fdfind --type f --type d --hidden --exclude .git"
else
    # Fallback to find (slower)
    SEARCH_CMD="find ~ -not -path '*/.git/*' -not -path '*/node_modules/*'"
fi

# Run fzf to select a file/dir.
# Start in the home directory
# Preview with 'bat' if available, or 'cat' for files, or 'ls -l' for dirs
SELECTED=$(eval "$SEARCH_CMD" 2>/dev/null | fzf --height 50% --border --preview 'bat --color=always {} 2>/dev/null || cat {} 2>/dev/null || ls -l {}')

if [[ -n "$SELECTED" ]]; then
    echo "Selected: $SELECTED"
else
    echo "Canceled."
fi
