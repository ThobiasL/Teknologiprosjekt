# Setup-fil for Linux

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

# Fullført oppsett-melding
echo "Oppsett ferdig. Husk å velge riktig tolk."
