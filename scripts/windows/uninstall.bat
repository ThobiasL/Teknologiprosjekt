@echo off
:: Script for avinstallering. Finner og sletter alle filer og mapper som ble opprettet under oppsett.

:: Kjør stop.bat for å stoppe alle prosesser
call "%~dp0stop.bat"

:: Slett __pycache__-mapper
for /d /r %%i in (__pycache__) do (
    echo Sletter mappe: %%i
    rmdir /s /q "%%i"
)

:: Slett .pyc-filer
for /r %%i in (*.pyc) do (
    echo Sletter fil: %%i
    del /q "%%i"
)

:: Slett .pytest_cache-mapper
for /d /r %%i in (.pytest_cache) do (
    echo Sletter mappe: %%i
    rmdir /s /q "%%i"
)

:: Slett .venv-mappen hvis den finnes
if exist .venv (
    echo Sletter .venv...
    rmdir /s /q .venv
)

:: Slett data-mappen hvis den finnes
if exist data (
    echo Sletter data...
    rmdir /s /q data
)

:: Slett Caddyfile hvis den finnes
if exist Caddyfile (
    echo Sletter Caddyfile...
    del /q Caddyfile
)

:: Slett .env hvis den finnes
if exist .env (
    echo Sletter .env...
    del /q .env
)

echo Avinstallering ferdig.
