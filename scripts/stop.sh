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

# Stopper Python-prosessen hvis den kjører (passer på å stoppe core.py)
if pgrep -f core/core.py > /dev/null; then
    echo "Stopper Python (core.py)..."
    pkill -f core/core.py
else
    echo "Python (core.py) kjører ikke."
fi

echo "Program stoppet."
