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

# Opprett instance-mappen hvis den ikke eksisterer
if [ ! -d "instance" ]; then
    mkdir instance
    echo "Opprettet instance-mappen."
fi

# Lager profiles.json med et tomt dictionary hvis den ikke eksisterer
if [ ! -f "instance/profiles.json" ]; then
    echo '{}' > instance/profiles.json
    echo "Opprettet profiles.json."
fi

# Lager lock.json hvis den ikke eksisterer
if [ ! -f "instance/lock.json" ]; then
    echo '{"lock_status" : 0, "lock_time" : "00:00"}' > instance/lock.json
    echo "Opprettet lock.json."
fi

# Fullført oppsett-melding
echo "Oppsett ferdig. Husk å velge riktig tolk."
