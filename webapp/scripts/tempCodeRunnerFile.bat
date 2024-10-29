:: Dette skriptet starter flask-webappen enkelt

:: Skjuler output fra kommandoer
@echo off

:: Bytter til webapp-mappen
cd webapp

:: Aktiverer virtuelt miljø
call .venv\Scripts\activate

:: Kjører flask sin run.py
python app.py
