@echo off
:: Script for å stoppe kjørende prosesser

:: Stopper Caddy hvis den kjører
tasklist /FI "IMAGENAME eq caddy.exe" | find /I "caddy.exe" >nul
if %errorlevel% equ 0 (
    echo Stopper Caddy...
    taskkill /IM caddy.exe /F
) else (
    echo Caddy kjører ikke.
)

:: Stopper Gunicorn hvis den kjører
tasklist /FI "IMAGENAME eq python.exe" | find /I "gunicorn" >nul
if %errorlevel% equ 0 (
    echo Stopper Gunicorn...
    for /f "tokens=2 delims= " %%i in ('tasklist /FI "IMAGENAME eq python.exe" /V ^| find "gunicorn"') do taskkill /PID %%i /F
) else (
    echo Gunicorn kjører ikke.
)

:: Stopper Python-prosessen hvis den kjører core.py
tasklist /FI "IMAGENAME eq python.exe" | find /I "core.py" >nul
if %errorlevel% equ 0 (
    echo Stopper Python (core.py)...
    for /f "tokens=2 delims= " %%i in ('tasklist /FI "IMAGENAME eq python.exe" /V ^| find "core.py"') do taskkill /PID %%i /F
) else (
    echo Python (core.py) kjører ikke.
)

echo Program stoppet.
