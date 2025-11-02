#!/usr/bin/env bash
# DESC: Auto-commit and push notes when changes exist
# TAG: git, notes, sync, backup, commit
# ARG: None - automatically detects changes
# EXAMPLE: jynotes

set -e

cd ~/Documents/UniNotes/MastersNotes || { echo "❌ Directory not found."; exit 1; }

LOGFILE="$HOME/Documents/UniNotes/auto_commit.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOGFILE"
}

if [ ! -d ".git" ]; then
    log "❌ Not a git repository. Exiting."
    exit 1
fi

git add .

COMMIT_MSG="Auto commit on $TIMESTAMP"
if git diff --cached --quiet; then
    log "⚠️  Nothing to commit (no changes)."
    exit 0
fi

git commit -m "$COMMIT_MSG" >/dev/null 2>&1

if git push >/dev/null 2>&1; then
    log "✅ Successfully pushed changes: '$COMMIT_MSG'"
else
    log "⚠️  Failed to push (check internet connection)."
fi
