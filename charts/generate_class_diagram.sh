#!/bin/bash

# Lager klassediagram for prosjektet

ROOT="$(dirname "$0")/.."
OUTPUT_DIR="$ROOT/charts"

export PATH=$PATH:/usr/bin

source "$ROOT/.venv/bin/activate"

pyreverse -o puml -p teknologiprosjekt -d "$OUTPUT_DIR" .
