#!/bin/bash

# Finn roten til prosjektet
ROOT="$(dirname "$0")/.."

# Aktiver virtuelt miljø
source "$ROOT/.venv/bin/activate"

# Caddyfile lages ved oppstart for å sikre at riktig IP-adresse brukes
CADDYFILE_PATH="$(pwd)/Caddyfile"

# IP-adressen til maskinen
IP_ADDRESS=$(hostname -I | awk '{print $1}')

# Skriver til Caddyfile med oppdatert IP-adresse
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

# Forsikrer at Caddyfile er formatert riktig
caddy fmt --overwrite Caddyfile 

# Starter caddy for HTTPS
caddy run --config "$ROOT/Caddyfile" --adapter caddyfile &

# Kjører wsgi-serveren med gunicorn og flask
gunicorn -c "$ROOT/server/gunicorn.config.py" server.wsgi:app &

# Printer ut adressen serveren kjører på for tilgang
echo "Server starter på følgende adresse:"
echo "https://$IP_ADDRESS:8443"
