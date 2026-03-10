#!/usr/bin/env bash
# DESC: Install all system, pip, and external dependencies required by JYScripts
# TAG: install, setup, dependencies, apt, pip, tools
# ARG: None - installs everything automatically, reports what needs manual setup
# EXAMPLE: jyinstall

set -euo pipefail

# ─────────────────────────────────────────
# COLOURS
# ─────────────────────────────────────────
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
RED="\033[1;31m"
CYAN="\033[1;36m"
RESET="\033[0m"

ok()   { echo -e "${GREEN}[✓]${RESET} $*"; }
info() { echo -e "${CYAN}[*]${RESET} $*"; }
warn() { echo -e "${YELLOW}[!]${RESET} $*"; }
fail() { echo -e "${RED}[✗]${RESET} $*"; }

ERRORS=()

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
apt_install() {
    for pkg in "$@"; do
        if dpkg -s "$pkg" &>/dev/null; then
            ok "$pkg already installed"
        else
            info "Installing $pkg..."
            if sudo apt-get install -y "$pkg" &>/dev/null; then
                ok "$pkg installed"
            else
                fail "$pkg failed to install"
                ERRORS+=("apt: $pkg")
            fi
        fi
    done
}

pip_install() {
    for pkg in "$@"; do
        if pip3 show "$pkg" &>/dev/null; then
            ok "pip: $pkg already installed"
        else
            info "pip installing $pkg..."
            if pip3 install --break-system-packages "$pkg" &>/dev/null; then
                ok "pip: $pkg installed"
            else
                fail "pip: $pkg failed"
                ERRORS+=("pip: $pkg")
            fi
        fi
    done
}

check_cmd() {
    if command -v "$1" &>/dev/null; then
        ok "$1 available"
    else
        warn "$1 not found — see manual steps below"
        ERRORS+=("manual: $1")
    fi
}

# ─────────────────────────────────────────
# START
# ─────────────────────────────────────────
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════╗${RESET}"
echo -e "${CYAN}║      JYScripts Dependency Installer      ║${RESET}"
echo -e "${CYAN}╚══════════════════════════════════════════╝${RESET}"
echo ""

# ─────────────────────────────────────────
# SYSTEM UPDATE
# ─────────────────────────────────────────
info "Updating apt package index..."
sudo apt-get update -qq
ok "Package index updated"

# ─────────────────────────────────────────
# CORE / SHARED DEPS
# Used by multiple scripts
# ─────────────────────────────────────────
info "Installing core utilities..."
apt_install \
    curl \
    jq \
    git \
    python3 \
    python3-pip \
    bash

# ─────────────────────────────────────────
# airpods.sh
# bluetoothctl (bluez), pactl (pulseaudio-utils)
# ─────────────────────────────────────────
info "Installing bluetooth + audio deps (airpods.sh)..."
apt_install \
    bluez \
    pulseaudio-utils

# ─────────────────────────────────────────
# arduino.sh / esp32.sh
# arduino-cli (manual), avr-gcc toolchain
# ─────────────────────────────────────────
info "Installing Arduino/ESP32 deps (arduino.sh, esp32.sh)..."
apt_install \
    gcc-avr \
    avr-libc \
    avrdude

if ! command -v arduino-cli &>/dev/null; then
    info "Installing arduino-cli..."
    if curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR="$HOME/.local/bin" sh &>/dev/null; then
        ok "arduino-cli installed to ~/.local/bin"
        export PATH="$HOME/.local/bin:$PATH"
        if ! grep -q 'HOME/.local/bin' "$HOME/.bashrc" 2>/dev/null; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
            warn "Added ~/.local/bin to PATH in .bashrc — restart shell or run: source ~/.bashrc"
        fi
    else
        fail "arduino-cli install failed — visit https://arduino.github.io/arduino-cli"
        ERRORS+=("manual: arduino-cli")
    fi
else
    ok "arduino-cli already available"
fi

# ─────────────────────────────────────────
# autocommit.py
# Uses only stdlib — no extra deps
# ─────────────────────────────────────────
ok "autocommit.py — stdlib only, no extra deps needed"

# ─────────────────────────────────────────
# bloat.py (jydiskbloat)
# Uses only stdlib — no extra deps
# ─────────────────────────────────────────
ok "bloat.py — stdlib only, no extra deps needed"

# ─────────────────────────────────────────
# bright.py (jybright)
# Uses only stdlib — needs udev rule for backlight write access
# ─────────────────────────────────────────
ok "bright.py — stdlib only"
if [ ! -f /etc/udev/rules.d/90-backlight.rules ]; then
    info "Setting up udev rule for backlight write access (bright.py)..."
    echo 'ACTION=="add", SUBSYSTEM=="backlight", KERNEL=="*", RUN+="/bin/chmod a+w /sys/class/backlight/%k/brightness"' \
        | sudo tee /etc/udev/rules.d/90-backlight.rules > /dev/null
    sudo udevadm control --reload-rules && sudo udevadm trigger
    ok "udev backlight rule created — takes effect on next reboot or hotplug"
else
    ok "udev backlight rule already exists"
fi

# ─────────────────────────────────────────
# chat.py (jychat)
# colorama
# ─────────────────────────────────────────
info "Installing chat.py deps..."
pip_install colorama

# ─────────────────────────────────────────
# checkhost.sh
# ping (iputils-ping)
# ─────────────────────────────────────────
info "Installing checkhost.sh deps..."
apt_install iputils-ping

# ─────────────────────────────────────────
# clip.sh
# xclip
# ─────────────────────────────────────────
info "Installing clip.sh deps..."
apt_install xclip

# ─────────────────────────────────────────
# define.sh
# curl, jq — already installed above
# ─────────────────────────────────────────
ok "define.sh — curl + jq already covered"

# ─────────────────────────────────────────
# env.sh (jyenv)
# conda — must be manually installed
# ─────────────────────────────────────────
if command -v conda &>/dev/null; then
    ok "conda already available"
else
    warn "conda not found (required by env.sh)"
    warn "Install Miniconda: https://docs.conda.io/en/latest/miniconda.html"
    ERRORS+=("manual: conda (miniconda/anaconda)")
fi

# ─────────────────────────────────────────
# etym.py (jyetym)
# urllib, html, re — all stdlib, no extra deps
# ─────────────────────────────────────────
ok "etym.py — stdlib only, no extra deps needed"

# ─────────────────────────────────────────
# find.sh (jyfind)
# fzf, fd-find, bat (optional preview)
# ─────────────────────────────────────────
info "Installing find.sh deps..."
apt_install fzf fd-find

if command -v fdfind &>/dev/null && ! command -v fd &>/dev/null; then
    mkdir -p "$HOME/.local/bin"
    ln -sf "$(which fdfind)" "$HOME/.local/bin/fd"
    ok "Created fd -> fdfind symlink in ~/.local/bin"
fi

if ! command -v bat &>/dev/null; then
    apt_install bat
    if command -v batcat &>/dev/null && ! command -v bat &>/dev/null; then
        ln -sf "$(which batcat)" "$HOME/.local/bin/bat"
        ok "Created bat -> batcat symlink in ~/.local/bin"
    fi
fi

# ─────────────────────────────────────────
# git.py (jygit)
# requests, rich
# Requires GITHUB_TOKEN env var
# ─────────────────────────────────────────
info "Installing git.py deps..."
pip_install requests rich

if [ -z "${GITHUB_TOKEN:-}" ]; then
    warn "GITHUB_TOKEN env var not set — required by git.py (jygit)"
    warn "Add to ~/.bashrc: export GITHUB_TOKEN=your_token_here"
    ERRORS+=("env_var: GITHUB_TOKEN")
fi

# ─────────────────────────────────────────
# matrix.sh (jymatrix)
# cmatrix, figlet
# ─────────────────────────────────────────
info "Installing matrix.sh deps..."
apt_install cmatrix figlet

# ─────────────────────────────────────────
# music.py (jymusic)
# spotipy, rich
# Requires SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET env vars
# ─────────────────────────────────────────
info "Installing music.py deps..."
pip_install spotipy rich

for var in SPOTIFY_CLIENT_ID SPOTIFY_CLIENT_SECRET; do
    if [ -z "${!var:-}" ]; then
        warn "$var env var not set — required by music.py (jymusic)"
        warn "Add to ~/.bashrc: export $var=your_value"
        ERRORS+=("env_var: $var")
    else
        ok "$var is set"
    fi
done

# ─────────────────────────────────────────
# myip.sh
# curl — already installed
# ─────────────────────────────────────────
ok "myip.sh — curl already covered"

# ─────────────────────────────────────────
# network.py (jynetcheck)
# speedtest-cli
# ─────────────────────────────────────────
info "Installing network.py deps..."
pip_install speedtest-cli

# ─────────────────────────────────────────
# notes.sh (jynotes)
# git — already installed
# Expects ~/Documents/UniNotes/MastersNotes to be a git repo
# ─────────────────────────────────────────
ok "notes.sh — git already covered"
if [ ! -d "$HOME/Documents/UniNotes/MastersNotes/.git" ]; then
    warn "~/Documents/UniNotes/MastersNotes is not a git repo — jynotes will fail"
    warn "Create or clone a repo there before using jynotes"
    ERRORS+=("setup: ~/Documents/UniNotes/MastersNotes git repo")
fi

# ─────────────────────────────────────────
# remind.sh
# notify-send (libnotify-bin)
# ─────────────────────────────────────────
info "Installing remind.sh deps..."
apt_install libnotify-bin

# ─────────────────────────────────────────
# ssh.py (jyssh)
# openssh-client, sshpass (optional)
# ─────────────────────────────────────────
info "Installing ssh.py deps..."
apt_install openssh-client sshpass

# ─────────────────────────────────────────
# sysinfo.sh (jysysinfo)
# upower, nvidia-smi (optional)
# ─────────────────────────────────────────
info "Installing sysinfo.sh deps..."
apt_install upower

if command -v nvidia-smi &>/dev/null; then
    ok "nvidia-smi available — GPU stats will work"
else
    warn "nvidia-smi not found — GPU section in jysysinfo will be skipped (expected if no NVIDIA GPU)"
fi

# ─────────────────────────────────────────
# translate.sh
# curl, jq — already installed
# ─────────────────────────────────────────
ok "translate.sh — curl + jq already covered"

# ─────────────────────────────────────────
# vpn.sh (jyvpn)
# protonvpn-cli, google-chrome (optional)
# ─────────────────────────────────────────
if command -v protonvpn &>/dev/null; then
    ok "protonvpn CLI available"
else
    warn "protonvpn CLI not found — required by vpn.sh"
    warn "Install from: https://protonvpn.com/support/linux-vpn-setup/"
    ERRORS+=("manual: protonvpn-cli")
fi

if command -v google-chrome &>/dev/null; then
    ok "google-chrome available"
else
    warn "google-chrome not found — vpn.sh incognito feature will fail"
    warn "Install from: https://www.google.com/chrome/"
    ERRORS+=("manual: google-chrome")
fi

# ─────────────────────────────────────────
# weather.sh
# curl — already installed
# ─────────────────────────────────────────
ok "weather.sh — curl already covered"

# ─────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════╗${RESET}"
echo -e "${CYAN}║                 Summary                  ║${RESET}"
echo -e "${CYAN}╚══════════════════════════════════════════╝${RESET}"

if [ ${#ERRORS[@]} -eq 0 ]; then
    echo -e "${GREEN}All dependencies installed successfully.${RESET}"
else
    echo -e "${YELLOW}Completed with ${#ERRORS[@]} item(s) needing manual attention:${RESET}"
    echo ""
    for err in "${ERRORS[@]}"; do
        case "$err" in
            apt:*)     fail "Package install failed:   ${err#apt: }" ;;
            pip:*)     fail "Pip install failed:       ${err#pip: }" ;;
            manual:*)  warn "Manual install required:  ${err#manual: }" ;;
            env_var:*) warn "Env var not set:          ${err#env_var: }" ;;
            setup:*)   warn "Setup needed:             ${err#setup: }" ;;
        esac
    done
    echo ""
    echo -e "${CYAN}Manual install links:${RESET}"
    echo "  conda:         https://docs.conda.io/en/latest/miniconda.html"
    echo "  protonvpn:     https://protonvpn.com/support/linux-vpn-setup/"
    echo "  google-chrome: https://www.google.com/chrome/"
    echo "  arduino-cli:   https://arduino.github.io/arduino-cli/latest/installation/"
fi

echo ""
echo -e "${CYAN}Post-install steps:${RESET}"
echo "  1. Reload your shell:  source ~/.bashrc"
echo "  2. Add env vars to ~/.bashrc if not already set:"
echo "       export GITHUB_TOKEN=..."
echo "       export SPOTIFY_CLIENT_ID=..."
echo "       export SPOTIFY_CLIENT_SECRET=..."
echo "  3. Run: sudo jyupdate   (installs all scripts to /usr/local/bin)"
echo ""
