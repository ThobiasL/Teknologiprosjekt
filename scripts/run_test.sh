#!/bin/bash

# Finn roten til prosjektet
ROOT="$(dirname "$0")/.."

# Aktiver virtuelt miljø
source "$ROOT/.venv/bin/activate"

pytest -v