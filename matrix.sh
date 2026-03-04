#!/usr/bin/env bash
# DESC: Randomized Matrix boot with original logs and cinematic decryption
# TAG: matrix, boot, terminal, greeting, ascii

set -euo pipefail






# Ensure the script only runs if a terminal is attached
if [ ! -t 0 ] && [ ! -t 1 ]; then
    exit 0
fi
