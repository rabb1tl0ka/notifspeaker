#!/bin/bash

# Check if the script is being sourced
if [ "$0" = "$BASH_SOURCE" ]; then
    echo "Error: This script should be sourced using 'source ./install-requirements.sh' or '.' ./install-requirements.sh'"
    echo "Exiting..."
    exit 1
fi

python3 -m venv .venv

source .venv/bin/activate && echo "Virtual environment activated successfully"

pip3 install -r requirements.txt
