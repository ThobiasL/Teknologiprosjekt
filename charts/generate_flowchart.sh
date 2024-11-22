#!/bin/bash

# Finn roten til prosjektet
ROOT="$(dirname "$0")/.."
OUTPUT_DIR="$ROOT/charts"

# Sørg for at OUTPUT_DIR eksisterer
mkdir -p "$OUTPUT_DIR"

# Aktiver virtuelt miljø
source "$ROOT/.venv/bin/activate"

# Kjør code2flow og lagre dot-filen i OUTPUT_DIR
xargs code2flow --language py --output "$OUTPUT_DIR/flowchart.dot" < "$OUTPUT_DIR/sources.txt"

# Konverter dot-filen til PNG og lagre i OUTPUT_DIR
dot -Tpng "$OUTPUT_DIR/flowchart.dot" -o "$OUTPUT_DIR/flowchart.png"

rm "$OUTPUT_DIR/flowchart.dot"
