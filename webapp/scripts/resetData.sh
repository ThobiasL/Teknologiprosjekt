# Script for å resette data-mappen

#!/bin/bash

# Bytt til webapp-mappen
cd webapp

# Slett data-mappen hvis den eksisterer
if [ -d "data" ]; then
    rm -rf data
fi

# Oppretter data-mappen med profiles.json og lock.json med default-verdier
mkdir data
echo '{}' > data/profiles.json
echo '{"lock_status" : 0, "lock_time" : "00:00"}' > data/lock.json


