from sendSignalToArduino import sendSignalToArduino
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
prev_alarm_mode = -1

editAlarm = 0
editAlarm_mode = 0

visit_mode = 0

def getDateTime():
    return strftime("%d.%m.%Y %H:%M")

def getTime():
    return strftime("%H:%M")

def update_alarm(signal):
    global hours, minutes

    if editAlarm == 1:
        if signal > 23:
            signal = 23
        hours = signal
        hours = f"{int(hours):02}" # :02 gjør om tallet til to-siffra
        sendSignalToArduino(hours, 0, 1)

    elif editAlarm == 2:
        if signal > 59:
            signal = 59
        minutes = signal
        minutes = f"{int(minutes):02}" # :02 gjør om tallet til to-siffra
        sendSignalToArduino(minutes, 3, 1)

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

    alarm_state = f"{hours}:{minutes}"
    if alarm_state == getTime():
        alarmTurnedOn = 1

    #Leser signal fra Arduino
    signal = readSignalFromArduino()

    if signal is not None:
        if signal == "alarm_mode: 1":
            alarm_mode = 1

        elif signal == "alarm_mode: 0":
            alarm_mode = 0

        elif signal == "editAlarm_mode: 1":
            editAlarm_mode = 1

        elif signal == "editAlarm_mode: 2":
            editAlarm_mode = 2

        elif signal == "editAlarm_mode: 0":
            editAlarm_mode = 0

        elif signal == "visit_mode: 1":
            visit_mode = 1

        elif signal == "visit_mode: 0":
            visit_mode = 0

        elif alarm_time == 1 and editAlarm_mode != 0:
            update_alarm(signal)

        else:
            volume_control(signal)


    if alarm_mode == 1 and prev_alarm_mode != 1:
        sendSignalToArduino("00:00", 0, 1)
        alarm_time = 1

    elif alarm_mode == 0 and prev_alarm_mode != 0:
        sendSignalToArduino("     ", 0, 1)
        alarm_time = 0
    prev_alarm_mode = alarm_mode

    if editAlarm_mode == 1:
        editAlarm = 1
    elif editAlarm_mode == 2:
        editAlarm = 2
    elif editAlarm_mode == 0:
        editAlarm = 0

    if visit_mode == 1:
        sendSignalToArduino("Besøks tid", 6, 1)
        #sende info til database
        visit_time = 1
    elif visit_mode == 0 and visit_time == 1:
        #sende info til database
        sendSignalToArduino("          ", 6, 1)
        visit_time = 0

    if alarmTurnedOn == 1 and alarm_mode == 1:
        alarmTimer += 1
        sendSignalToArduino("Alarm!", 6, 1)
        # avspilling av alarm lyd
        if alarmTimer == 10:
            sendSignalToArduino("      ", 6, 1)
            alarmTimer = 0
            alarmTurnedOn = 0

    sleep(0.1)