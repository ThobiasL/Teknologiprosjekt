# Config-fil for Gunicorn

# Binder serveren til localhost på port 8000, for å begrense tilgang fra andre enheter
bind = "127.0.0.1:8000"

# Antall prosesser for håndtering av forespørsler
workers = 4

# Timeout for en arbeiderprosess på 120 sekunder
timeout = 120  

# Loggnivå
loglevel = "info"

# Logg tilgang i konsollen
accesslog = "-"

# Logg feil i konsollen
errorlog = "-"

# Navn på prosessen
proc_name = "GunicornServer"
