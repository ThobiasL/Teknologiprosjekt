:: Setup-fil for Windows

@echo off

:: Bytt til webapp-mappen
cd webapp

:: # Opprett virtuelt miljø
echo Oppretter virtuelt miljø i .venv...
python -m venv .venv

:: # Aktiver virtuelt miljø
echo Aktiverer virtuelt miljø...
call .venv\Scripts\activate

:: # Installerer avhengigheter
pip install -r requirements.txt

:: # Fullført oppsett-melding
echo Oppsett ferdig. Husk å velge riktig tolk.
