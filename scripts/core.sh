#!/bin/bash

# Finn roten til prosjektet
ROOT="$(dirname "$0")/.."

# Aktiver virtuelt miljø
source "$ROOT/.venv/bin/activate"

export PYTHONPATH=$(pwd) # Sett PYTHONPATH til root

# Start Python skriptet
python services/core.py
