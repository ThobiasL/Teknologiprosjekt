#!/bin/bash

# Stopper Caddy hvis den kjører
if pgrep -f caddy > /dev/null; then
    echo "Stopper Caddy..."
    caddy stop
else
    echo "Caddy kjører ikke."
fi

# Stopper Gunicorn hvis den kjører
if pgrep -f gunicorn > /dev/null; then
    echo "Stopper Gunicorn..."
    pkill -f gunicorn
else
    echo "Gunicorn kjører ikke."
fi

echo "Server stoppet."
