from sendSignalToArduino import sendSignalToArduino, clearLCD
from ReadSignalFromArduino import readSignalFromArduino
from time import sleep, strftime

#Knappe variabler
alarm_time = 0
visit_time = 0

#Alarm variabler
hours = 0
minutes = 0
alarm_mode = 0
alarm_state = f"{hours}:{minutes}"
alarmTurnedOn = 0
alarmTimer = 0

editAlarm = 0
editAlarm_mode = 0

visit_mode = 0

def getDateTime():
    dateTime = strftime("%d.%m.%Y %H:%M")
    return dateTime

def getTime():
    time = strftime("%H:%M")
    return time

def update_alarm(readSignalFromArduino):
    if editAlarm == 0:
        hours = readSignalFromArduino
        if hours < 10:
            hours = "0" + hours
        time = f"{hours}:{minutes}"
        sendSignalToArduino(time, 0, 1)

    elif editAlarm == 1:
        minutes = readSignalFromArduino
        if minutes < 10:
            minutes = "0" + minutes
        time = f"{hours}:{minutes}"
        sendSignalToArduino(time, 0, 1)

def volume_control(readSignalFromArduino):
    volume = readSignalFromArduino
    prosent = f"{volume}%"
    if volume == 100:
        sendSignalToArduino(prosent, 13, 1)
    else:
        sendSignalToArduino(prosent, 14, 1)


while True:

    DateNow = getDateTime()
    timeNow = getTime()
    sendSignalToArduino(DateNow, 0, 0)

    if alarm_state == timeNow:
        alarmTurnedOn = 1

    #Leser signal fra Arduino
    if readSignalFromArduino == "alarm_mode: 1":
        alarm_mode = 1

    elif readSignalFromArduino == "editAlarm_mode: 1":
        editAlarm_mode = 1

    elif readSignalFromArduino == "visit_mode: 1":
        visit_mode = 1

    elif alarm_time == 1:
        update_alarm(readSignalFromArduino)

    else:
        volume_control(readSignalFromArduino)


    if alarm_mode == 1 & alarm_time == 0:
        sendSignalToArduino("00:00", 0, 1)
        alarm_time = 1

    elif alarm_mode == 1 & alarm_time == 1:
        alarm_time = 0

    if editAlarm_mode == 1 & editAlarm == 0:
        editAlarm = 1

    elif editAlarm_mode == 1 & editAlarm == 1:
        clearLCD()
        editAlarm = 0

    if visit_mode == 1 & visit_time == 0:
        sendSignalToArduino("Besøks tid", 7, 1)
        #sende info til database
        visit_time = 1

    elif visit_mode == 1 & visit_time == 1:
        #sende info til database
        clearLCD()
        visit_time = 0

    if alarmTurnedOn == 1 & alarm_mode == 1:
        alarmTimer += 1
        sendSignalToArduino("Alarm", 7, 1)
        # avspilling av alarm lyd
        if alarmTimer == 10:
            clearLCD()
            alarmTimer = 0

    sleep(0.1)