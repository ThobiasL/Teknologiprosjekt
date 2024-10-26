:: Script for å resette data-mappen

:: Skjuler output fra kommandoene
@echo off

:: Bytt til webapp-mappen
cd webapp

:: Slett data-mappen hvis den eksisterer
if exist data (
    rmdir /s /q data
)

:: Oppretter data-mappen med profiles.json og lock.json med default-innhold
mkdir data
echo {} > data\profiles.json
echo {"lock_status" : 0, "lock_time" : "00:00"} > data\lock.json
