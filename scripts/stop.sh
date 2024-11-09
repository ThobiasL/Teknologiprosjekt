#!/bin/bash

# Stopper Caddy hvis den kjører
if pgrep -f caddy > /dev/null; then
    echo "Stopping Caddy..."
    caddy stop
else
    echo "Caddy is not running."
fi

# Stopper Gunicorn hvis den kjører
if pgrep -f gunicorn > /dev/null; then
    echo "Stopping Gunicorn..."
    pkill -f gunicorn
else
    echo "Gunicorn is not running."
fi

echo "Server stoppet."
