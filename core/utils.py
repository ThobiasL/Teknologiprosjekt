from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Sjekker om tid følger formatet HH:MM, og returnerer False hvis ikke
def is_valid_time(value):
    try:
        datetime.strptime(value, '%H:%M')
        return True
    except ValueError:
        return False

# Hasher passord
def hash_password(password):
    return generate_password_hash(password)

# Sjekker passord-hash
def verify_password(password_hash, password):
    return check_password_hash(password_hash, password)

    