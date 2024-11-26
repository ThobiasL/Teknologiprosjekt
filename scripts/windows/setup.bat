@echo off
:: Script for oppsett av webapp på Windows

:: Stopp ved feil
setlocal enabledelayedexpansion
set ERRORLEVEL=0

:: Funksjon for å rydde opp ved feil
:cleanup
echo Feil oppstod. Rydder opp...
call "%~dp0uninstall.bat"
exit /b 1

:: Sett trap for feil
if ERRORLEVEL 1 (
    call :cleanup
)

:: Gå til root
cd /d "%~dp0.."

:: Sett PYTHONPATH til root
set PYTHONPATH=%cd%

:: Opprett virtuelt miljø
echo Oppretter virtuelt miljø i .venv...
python -m venv .venv || goto :cleanup

:: Aktiver virtuelt miljø
echo Aktiverer virtuelt miljø...
call ".venv\Scripts\activate.bat" || goto :cleanup

:: Installerer avhengigheter
echo Installerer avhengigheter fra requirements.txt...
pip install -r requirements.txt || goto :cleanup

:: Sjekk og installer Caddy
where caddy >nul 2>&1
if %errorlevel% neq 0 (
    echo Installerer Caddy...
    powershell -Command "Start-Process cmd -ArgumentList '/c winget install CaddyServer.Caddy' -Verb runAs" || goto :cleanup
) else (
    echo Caddy er allerede installert.
)

:: Generer SECRET_KEY
for /f "tokens=*" %%i in ('python -c "import secrets; print(secrets.token_urlsafe(32))"') do set SECRET_KEY=%%i

if not exist .env (
    echo.>.env
)

:: Legg til SECRET_KEY i .env hvis den ikke finnes
findstr /c:"SECRET_KEY" .env >nul 2>&1
if %errorlevel% neq 0 (
    echo SECRET_KEY=%SECRET_KEY%>>.env
    echo SECRET_KEY lagt til i .env
) else (
    echo SECRET_KEY finnes allerede i .env
)

:: Kjører setup_db.py for å sette opp databasen
python -m adapters.database.setup_db || goto :cleanup

:: Fullført oppsett-melding
echo Oppsett ferdig. Husk å velge riktig tolk.
exit /b 0
