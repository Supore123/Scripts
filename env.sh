#!/usr/bin/env bash
# DESC: Simplified Conda environment manager (list, create, activate, delete, info)
# TAG: conda, python, environment, virtualenv, management
# ARG: [command] [name] - Command: list|create|activate|delete|info
# EXAMPLE: jyenv list
# EXAMPLE: jyenv create myenv python=3.10
# EXAMPLE: jyenv activate myenv
# EXAMPLE: jyenv delete myenv
# EXAMPLE: jyenv info

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Ensure conda exists
if ! command -v conda >/dev/null 2>&1; then
    echo -e "${RED}Error:${NC} Conda not found in PATH."
    echo "Please install Miniconda or Anaconda first."
    exit 1
fi

command="$1"
env_name="$2"
extra="$3"

function list_envs() {
    echo -e "${CYAN}Available Conda environments:${NC}"
    conda env list | sed 's/^/  /'
}

function create_env() {
    if [ -z "$env_name" ]; then
        echo -e "${YELLOW}Usage:${NC} jyenv create <name> [python=3.x]"
        return
    fi
    echo -e "${CYAN}Creating environment:${NC} $env_name $extra"
    conda create -y -n "$env_name" $extra
}

function activate_env() {
    if [ -z "$env_name" ]; then
        echo -e "${YELLOW}Usage:${NC} jyenv activate <name>"
        return
    fi
    echo -e "${GREEN}Activating environment:${NC} $env_name"
    eval "$(conda shell.bash hook)"
    conda activate "$env_name"
}

function delete_env() {
    if [ -z "$env_name" ]; then
        echo -e "${YELLOW}Usage:${NC} jyenv delete <name>"
        return
    fi
    echo -e "${RED}Deleting environment:${NC} $env_name"
    conda env remove -n "$env_name" -y
}

function env_info() {
    if [ -z "$env_name" ]; then
        echo -e "${CYAN}Current environment info:${NC}"
        conda info
    else
        echo -e "${CYAN}Packages in:${NC} $env_name"
        conda list -n "$env_name"
    fi
}

case "$command" in
    list|"")
        list_envs
        ;;
    create)
        create_env
        ;;
    activate)
        activate_env
        ;;
    delete)
        delete_env
        ;;
    info)
        env_info
        ;;
    *)
        echo -e "${YELLOW}Usage:${NC} jyenv [list|create|activate|delete|info] [env_name]"
        ;;
esac

