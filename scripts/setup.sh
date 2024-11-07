# Script for oppsett av webapp på Linux

#!/bin/bash

set -e # Avslutt scriptet ved første feil

# Funksjon for å rydde opp ved feil
cleanup() {
    echo "Feil oppstod. Rydder opp..."
    bash "$(dirname "$0")/uninstall.sh"
}

trap cleanup ERR # Kjør cleanup-funksjonen ved feil

cd "$(dirname "$0")/.." # Gå til root

export PYTHONPATH=$(pwd) # Sett PYTHONPATH til root

# Opprett virtuelt miljø
echo "Oppretter virtuelt miljø i .venv..."
python3 -m venv .venv

# Aktiver virtuelt miljø
echo "Aktiverer virtuelt miljø..."
source .venv/bin/activate

# Installerer avhengigheter
echo "Installerer avhengigheter 

fra requirements.txt..."
pip install -r requirements.txt

# Kjører setup_db.py for å sette opp databasen
python3 -m database.setup_db

# Fullført oppsett-melding
echo "Oppsett ferdig. Husk å velge riktig tolk."



