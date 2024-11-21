#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)

# Finn roten til prosjektet
ROOT="$(dirname "$0")/.."

# Aktiver virtuelt miljø
source "$ROOT/.venv/bin/activate"

pytest -v --capture=no