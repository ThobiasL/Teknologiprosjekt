#!/bin/bash

# Finn roten til prosjektet
ROOT="$(dirname "$0")/.."

export PATH=$PATH:/usr/bin

# Aktiver virtuelt miljø
source "$ROOT/.venv/bin/activate"

pyreverse -o dot -p Teknologiprosjekt .
