from datetime import datetime

# Sjekker om tid følger formatet HH:MM, og returnerer False hvis ikke
def is_valid_time(value):
    try:
        datetime.strptime(value, '%H:%M')
        return True
    except ValueError:
        return False