:: Fil for oppsett av webapp på Windows

:: Skjuler output fra kommandoer
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

:: Opprett data-mappen hvis den ikke eksisterer
if not exist data (
    mkdir data
    echo Opprettet data-mappen
)

:: Opprett profiles.json med et tomt dictionary i data-mappen hvis den ikke eksisterer
if not exist data\profiles.json (
    echo {} > data\profiles.json
    echo Opprettet profiles.json
)

:: Opprett lock_status.json med lock_status lik 0 (ulåst) i data-mappen hvis den ikke eksisterer
if not exist data\lock.json (
    echo {"lock_status" : 0, "lock_time" : "00:00"} > data\lock.json
    echo Opprettet lock.json med ulåst status.
)

:: # Fullført oppsett-melding
echo Oppsett ferdig. Husk å velge riktig tolk.
