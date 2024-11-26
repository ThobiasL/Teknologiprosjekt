@echo off
:: Script for å kjøre tester med pytest

:: Sett PYTHONPATH til nåværende katalog
set PYTHONPATH=%PYTHONPATH%;%cd%

:: Finn roten til prosjektet
set ROOT=%~dp0..

:: Aktiver virtuelt miljø
call "%ROOT%\.venv\Scripts\activate.bat"

:: Kjør pytest med detaljerte utdata
pytest -v --capture=no
