#!/bin/bash

# Finn roten til prosjektet
ROOT="$(dirname "$0")/.."

# Aktiver virtuelt miljø
source "$ROOT/.venv/bin/activate"

# Naviger til prosjektets rotmappe for å unngå relative sti-problemer
cd "$ROOT" || exit

# Sett PYTHONPATH til prosjektets rotmappe
export PYTHONPATH=$(pwd)

# Kontroller at miljøet er riktig konfigurert
echo "PYTHONPATH: $PYTHONPATH"
echo "Python versjon: $(python --version)"

# Start Python-skriptet
python core/core.py
