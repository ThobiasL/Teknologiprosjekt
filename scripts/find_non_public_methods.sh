#!/bin/bash

# Rotkatalog der Python-filer skal analyseres
ROOT_DIR=${1:-.}

if [[ ! -d "$ROOT_DIR" ]]; then
    echo "Bruk: $0 <katalog>"
    exit 1
fi

echo "Søker etter Python-filer i: $ROOT_DIR (ekskluderer .venv)"

# Finn alle Python-filer og ekskluder .env-mappen
find "$ROOT_DIR" -type f -name "*.py" -not -path "*/.venv/*" | while read -r PYTHON_FILE; do
    # Sjekk om filen inneholder beskyttede eller private funksjoner
    PROTECTED_FUNCTIONS=$(grep -E '^\s*def _[^_]+' "$PYTHON_FILE")
    PRIVATE_FUNCTIONS=$(grep -E '^\s*def __[^_]+[^_]' "$PYTHON_FILE")

    if [[ -n "$PROTECTED_FUNCTIONS" || -n "$PRIVATE_FUNCTIONS" ]]; then
        echo "======================================="
        echo "Fil: $PYTHON_FILE"
        
        if [[ -n "$PROTECTED_FUNCTIONS" ]]; then
            echo "Beskyttede funksjoner:"
            echo "$PROTECTED_FUNCTIONS" | awk '{print "  - " $2}' | sed 's/(.*//'
        fi
        
        if [[ -n "$PRIVATE_FUNCTIONS" ]]; then
            echo "Private funksjoner:"
            echo "$PRIVATE_FUNCTIONS" | awk '{print "  - " $2}' | sed 's/(.*//'
        fi
        echo
    fi
done
