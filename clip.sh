#!/bin/bash

# If there's piped input, read it
if [ ! -t 0 ]; then
    xclip -selection clipboard
    exit 0
fi

# Otherwise, use arguments
if [ $# -gt 0 ]; then
    printf "%s" "$*" | xclip -selection clipboard
    exit 0
fi

echo "Usage:"
echo "  echo 'hello' | clip.sh"
echo "  clip.sh 'hello world'"
exit 1

