#!/usr/bin/env bash
# DESC: Quick reference helper for jy commands
# TAG: help, quick, reference, cheatsheet
# ARG: [command] - Show quick help for specific command
# EXAMPLE: jyhelper music
# EXAMPLE: jyhelper

set -euo pipefail

show_quick_help() {
    local cmd="$1"
    case "$cmd" in
        music)
            echo "🎵 JYmusic Quick Reference:"
            echo "  jymusic                    - Show status"
            echo "  jymusic 'song name'        - Play song"
            echo "  jymusic next               - Skip track"
            echo "  jymusic pause              - Pause"
            echo "  jymusic vol 80             - Set volume"
            echo "  jymusic shuffle            - Toggle shuffle"
            ;;
        airpods)
            echo "🎧 JYairpods Quick Reference:"
            echo "  jyairpods                  - Connect/disconnect"
            echo "  jyairpods <MAC>            - Connect specific device"
            ;;
        ssh)
            echo "🔐 JYssh Quick Reference:"
            echo "  jyssh --list               - List saved hosts"
            echo "  jyssh --add                - Add new host"
            echo "  jyssh --host <name>        - Connect to host"
            ;;
        *)
            echo "❓ Unknown command: $cmd"
            echo "Try: jyhelp"
            ;;
    esac
}

if [ $# -eq 0 ]; then
    echo "📋 JY Commands Cheatsheet"
    echo ""
    echo "🎵 Music:      jymusic [song/next/pause/vol]"
    echo "🎧 Bluetooth:  jyairpods"
    echo "💻 System:     jysysinfo"
    echo "📝 Notes:      jynotes"
    echo "🔐 SSH:        jyssh --list"
    echo "🔧 Utils:      jyutils [disk/mem/date]"
    echo "💬 Chat:       jychat"
    echo ""
    echo "For details: jyhelper <command>"
else
    show_quick_help "$1"
fi
