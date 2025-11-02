
##!/usr/bin/env
# DESC: Smart script to auto-commit and push
#              your notes only when changes exist.
# Author: Jonathan Yohannes
# ===============================================

# Exit immediately if any command fails
set -e

# Go to Notes directory
cd ~/Documents/UniNotes/MastersNotes || { echo "❌ Directory not found."; exit 1; }

# Log file path
LOGFILE="$HOME/Documents/UniNotes/auto_commit.log"

# Timestamp for messages
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Function to write logs
log() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOGFILE"
}

# Ensure it's a git repository
if [ ! -d ".git" ]; then
    log "❌ Not a git repository. Exiting."
    exit 1
fi

# Add all changes
git add .

# Create commit message
COMMIT_MSG="Auto commit on $TIMESTAMP"
git commit -m "$COMMIT_MSG" >/dev/null 2>&1 || {
    log "⚠️  Nothing to commit (maybe empty changes)."
    exit 0
}

# Try pushing to remote
if git push >/dev/null 2>&1; then
    log "✅ Successfully pushed changes: '$COMMIT_MSG'"
else
    log "⚠️  Failed to push changes (maybe no internet). Will retry next time."
fi


