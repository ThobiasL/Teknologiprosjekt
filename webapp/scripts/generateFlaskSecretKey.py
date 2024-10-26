import os

# Genererer en tilfeldig streng på 24 bytes som kan brukes som secret key i Flask
print(os.urandom(24))
