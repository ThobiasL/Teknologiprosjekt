:: Setup-fil for Windows

@echo off

:: Bytt til webapp-mappen
cd webapp

:: # Opprett virtuelt miljø
echo Oppretter virtuelt miljø i .venv om det ikke eksisterer...
if not exist .venv (
    python -m venv .venv
    echo Opprettet .venv
)

:: # Aktiver virtuelt miljø
echo Aktiverer virtuelt miljø...
call .venv\Scripts\activate

:: # Installerer avhengigheter
pip install -r requirements.txt

:: Opprett instance-mappen hvis den ikke eksisterer
if not exist instance (
    mkdir instance
    echo Opprettet instance-mappen
)

:: Opprett profiles.json med et tomt dictionary i instance-mappen hvis den ikke eksisterer
if not exist instance\profiles.json (
    echo {} > instance\profiles.json
    echo Opprettet profiles.json
)

:: Opprett lock_status.json med lock_status lik 0 (ulåst) i instance-mappen hvis den ikke eksisterer
if not exist instance\lock.json (
    echo {"lock_status" : 0, "lock_time" : "00:00"} > instance\lock.json
    echo Opprettet lock.json med ulåst status.
)

:: # Fullført oppsett-melding
echo Oppsett ferdig. Husk å velge riktig tolk.
