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

:: # Fullført oppsett-melding
echo Oppsett ferdig. Husk å velge riktig tolk.
