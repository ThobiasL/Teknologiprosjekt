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
echo "Installerer avhengigheter fra requirements.txt..."
pip install -r requirements.txt

# Installerer Caddy for HTTPS hvis ikke allerede installert
if ! command -v caddy &> /dev/null
then
    echo "Installerer Caddy..."
    
    # Legger til nødvendige pakker og nøkler for å installere Caddy
    sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
    
    # Oppdaterer pakkelisten og installerer Caddy
    sudo apt update
    sudo apt install caddy
else
    echo "Caddy er allerede installert."
fi

SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

if [ ! -f .env ]; then
    touch .env
fi

if grep -q "SECRET_KEY" .env; then
    echo "SECRET_KEY finnes allerede i .env"
else
    echo "SECRET_KEY=$SECRET_KEY" >> .env
    echo "SECRET_KEY lagt til i .env"
fi

# Kjører setup_db.py for å sette opp databasen
python3 -m adapters.database.setup_db

# Fullført oppsett-melding
echo "Oppsett ferdig. Husk å velge riktig tolk."



