@echo off
:: Bytter til webapp-mappen
cd webapp

:: Aktiverer virtuelt miljø
call .venv\Scripts\activate

:: Kjører flask sin run.py
python run.py
