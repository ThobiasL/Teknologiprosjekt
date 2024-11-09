# Finn roten til prosjektet
ROOT="$(dirname "$0")/.."

# Aktiver virtuelt miljø
source "$ROOT/.venv/bin/activate"

gunicorn -c "$ROOT/server/gunicorn.config.py" server.wsgi:app &


