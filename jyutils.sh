#!/usr/bin/env bash
# DESC: General utility script with helpful commands
# ARG: echo <message> - Print a message to the terminal
# ARG: clear - Clear the terminal screen
# ARG: date - Show current date and time
# ARG: disk - Show disk usage
# ARG: mem - Show memory usage
# ARG: ls [dir] - List files in a directory (default current)
# ARG: help - Show available utility commands

set -euo pipefail

# Helper: Show utility commands
jyutils_help() {
    echo "Available jyutils commands:"
    echo "  echo <message>   - Print a message"
    echo "  clear            - Clear the screen"
    echo "  date             - Show date and time"
    echo "  disk             - Show disk usage"
    echo "  mem              - Show memory usage"
    echo "  ls [dir]         - List files in directory (default current)"
    echo "  help             - Show this help message"
}

# Parse first argument
cmd="${1:-help}"
shift || true

case "$cmd" in
    echo)
        echo "$*"
        ;;
    clear)
        clear
        ;;
    date)
        date
        ;;
    disk)
        df -h
        ;;
    mem)
        free -h
        ;;
    ls)
        dir="${1:-.}"
        ls -lh "$dir"
        ;;
    help|*)
        jyutils_help
        ;;
esac

