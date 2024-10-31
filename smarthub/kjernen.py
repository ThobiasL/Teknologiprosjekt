from sendSignalToArduino import sendSignalToArduino, clearLCD
from ReadSignalFromArduino import readSignalFromArduino
from time import sleep, strftime

#Knappe variabler
alarm_time = 0
visit_time = 0

#Alarm variabler
hours = "00"
minutes = "00"
alarm_mode = 0
alarm_state = f"{hours}:{minutes}"
alarmTurnedOn = 0
alarmTimer = 0

editAlarm = 0
editAlarm_mode = 0

visit_mode = 0

def getDateTime():
    return strftime("%d.%m.%Y %H:%M")

def getTime():
    return strftime("%H:%M")

def update_alarm(signal):
    if editAlarm == 0:
        hours = signal
        if hours < 10:
            hours = "0" + hours
        time = f"{hours}:{minutes}"
        sendSignalToArduino(time, 0, 1)

    elif editAlarm == 1:
        minutes = signal
        if minutes < 10:
            minutes = "0" + minutes
        time = f"{hours}:{minutes}"
        sendSignalToArduino(time, 0, 1)

def volume_control(signal):
    if volume >= 100:
        volume_prosent = f"{signal}%"
    elif signal >= 10:
        volume_prosent = f" {signal}%"
    else:
        volume_prosent = f"  {signal}%"
    sendSignalToArduino(volume_prosent, 12, 1)


while True:
    sendSignalToArduino(getDateTime(), 0, 0)

    if alarm_state == getTime():
        alarmTurnedOn = 1

    #Leser signal fra Arduino
    signal = readSignalFromArduino()

    if signal is not None:
        if signal == "alarm_mode: 1":
            alarm_mode = 1

        elif signal == "editAlarm_mode: 1":
            editAlarm_mode = 1

        elif signal == "visit_mode: 1":
            visit_mode = 1

        elif alarm_time == 1:
            update_alarm(signal)

        else:
            volume_control(signal)


    if alarm_mode == 1 & alarm_time == 0:
        sendSignalToArduino("00:00", 0, 1)
        alarm_time = 1

    elif alarm_mode == 1 & alarm_time == 1:
        sendSignalToArduino("     ", 0, 1)
        alarm_time = 0

    if editAlarm_mode == 1 & editAlarm == 0:
        editAlarm = 1

    elif editAlarm_mode == 1 & editAlarm == 1:
        editAlarm = 0

    if visit_mode == 1 & visit_time == 0:
        sendSignalToArduino("Besøks tid", 7, 1)
        #sende info til database
        visit_time = 1

    elif visit_mode == 1 & visit_time == 1:
        #sende info til database
        sendSignalToArduino("          ", 7, 1)
        visit_time = 0

    if alarmTurnedOn == 1 & alarm_mode == 1:
        alarmTimer += 1
        sendSignalToArduino("Alarm!", 7, 1)
        # avspilling av alarm lyd
        if alarmTimer == 10:
            sendSignalToArduino("      ", 7, 1)
            alarmTimer = 0
            alarmTurnedOn = 0

    sleep(0.1)