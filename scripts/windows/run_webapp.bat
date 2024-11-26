:: Finn roten til prosjektet
set ROOT=%~dp0..

:: Aktiver virtuelt miljø
call "%ROOT%\.venv\Scripts\activate.bat"

:: Caddyfile lages ved oppstart for å sikre at riktig IP-adresse brukes
set CADDYFILE_PATH=%cd%\Caddyfile

:: Finn IP-adressen til maskinen (krever PowerShell)
for /f "usebackq tokens=*" %%i in (`powershell -Command "(Get-NetIPAddress -AddressFamily IPv4).IPAddress | Select-Object -First 1"`) do set IP_ADDRESS=%%i

:: Skriver til Caddyfile med oppdatert IP-adresse
echo { > "%CADDYFILE_PATH%"
echo     http_port 8080 >> "%CADDYFILE_PATH%"
echo     https_port 8443 >> "%CADDYFILE_PATH%"
echo } >> "%CADDYFILE_PATH%"
echo http://%IP_ADDRESS%:8080 { >> "%CADDYFILE_PATH%"
echo     redir https://{host}:8443{uri} >> "%CADDYFILE_PATH%"
echo } >> "%CADDYFILE_PATH%"
echo https://%IP_ADDRESS%:8443 { >> "%CADDYFILE_PATH%"
echo     reverse_proxy localhost:8000 >> "%CADDYFILE_PATH%"
echo     tls internal >> "%CADDYFILE_PATH%"
echo } >> "%CADDYFILE_PATH%"

:: Forsikrer at Caddyfile er formatert riktig
caddy fmt --overwrite Caddyfile

:: Starter caddy for HTTPS
start caddy run --config "%ROOT%\Caddyfile" --adapter caddyfile

:: Kjører wsgi-serveren med gunicorn og flask
start gunicorn -c "%ROOT%\server\gunicorn.config.py" server.wsgi:app

:: Printer ut adressen serveren kjører på for tilgang
echo Server starter på følgende adresse:
echo https://%IP_ADDRESS%:8443
