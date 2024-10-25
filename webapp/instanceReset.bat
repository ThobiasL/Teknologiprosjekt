@echo off

cd webapp

if exist instance (
    rmdir /s /q instance
    mkdir instance
    echo {} > instance\profiles.json
    echo {"lock_status" : 0, "lock_time" : "00:00"} > instance\lock.json
)