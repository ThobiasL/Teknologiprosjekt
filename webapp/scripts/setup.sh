# Fil for oppsett av webapp på Linux

#!/bin/bash

# Bytt til webapp-mappen
cd webapp

# Opprett virtuelt miljø
echo "Oppretter virtuelt miljø i .venv..."
python3 -m venv .venv

# Aktiver virtuelt miljø
echo "Aktiverer virtuelt miljø..."
source .venv/bin/activate

# Installerer avhengigheter
echo "Installerer avhengigheter fra requirements.txt..."
pip install -r requirements.txt

# Opprett data-mappen hvis den ikke eksisterer
if [ ! -d "data" ]; then
    mkdir data
    echo "Opprettet data-mappen."
fi

# Lager profiles.json med et tomt dictionary hvis den ikke eksisterer
if [ ! -f "data/profiles.json" ]; then
    echo '{}' > data/profiles.json
    echo "Opprettet profiles.json."
fi

# Lager lock.json hvis den ikke eksisterer
if [ ! -f "data/lock.json" ]; then
    echo '{"lock_status" : 0, "lock_time" : "00:00"}' > data/lock.json
    echo "Opprettet lock.json."
fi

# Fullført oppsett-melding
echo "Oppsett ferdig. Husk å velge riktig tolk."
