#!/bin/bash

# Finn roten til prosjektet
ROOT="$(dirname "$0")/.."

# Aktiver virtuelt miljø
source "$ROOT/.venv/bin/activate"

# Caddyfile lages ved oppstart for å sikre at riktig IP-adresse brukes
CADDYFILE_PATH="$(pwd)/Caddyfile"
if [ ! -f Caddyfile ]; then
    echo "Oppretter eller oppdaterer Caddyfile..."

    IP_ADDRESS=$(hostname -I | awk '{print $1}')

    echo "
{
    http_port 8080
    https_port 8443
}

# HTTP (port 8080)
http://$IP_ADDRESS:8080 {
    redir https://{host}:8443{uri}
}

# HTTPS (port 8443)
https://$IP_ADDRESS:8443 {
    reverse_proxy localhost:8000
    tls internal
}
" > "$CADDYFILE_PATH"

caddy fmt --overwrite Caddyfile # Forsikrer at Caddyfile er formatert riktig

else
    echo "Caddyfile eksisterer allerede."
    
fi

# Starter caddy for HTTPS
caddy run --config "$ROOT/Caddyfile" --adapter caddyfile &

# Kjører wsgi-serveren med gunicorn og flask
gunicorn -c "$ROOT/server/gunicorn.config.py" server.wsgi:app &

# Maskinens IP-adresse for tilgang
IP_ADDRESS=$(hostname -I | awk '{print $1}')
echo "Server starter på følgende adresse:"
echo "https://$IP_ADDRESS:8443"
