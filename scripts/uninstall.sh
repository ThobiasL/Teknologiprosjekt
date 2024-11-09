# Script for avinstallering. Finner og sletter alle filer og mapper som ble opprettet under oppsett.

#!/bin/bash

bash "$(dirname "$0")/stop.sh"

find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -exec rm -f {} +
find . -type d -name ".pytest_cache" -exec rm -rf {} +

if [ -d .venv ]; then
    rm -rf .venv
fi

if [ -d data ]; then
    rm -rf data
fi

if [ -f Caddyfile ]; then
    rm Caddyfile
fi

if [ -f .env ]; then
    rm .env
fi

echo "Avinstallering ferdig."