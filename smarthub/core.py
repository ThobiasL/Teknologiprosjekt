from CommunicationWithExternalDevices import ExternalDevicesCommunication
from CommunicationWithDatabase import DatabaseCommunication
from CommunicationWithFrontend import FrontendCommunication
from CommunicationWithArduino import ArduinoSerial
from adjustingVolume import SoundPlayer
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
prev_vivit_mode = -1

#kaller på funksjonene fra klassen ExternalDevicesCommunication
externalDevices = ExternalDevicesCommunication()
#kaller på funksjonene fra klassen DatabaseCommunication
database = DatabaseCommunication()
#kaller på funksjonene fra klassen FrontendCommunication
frontend = FrontendCommunication()
#kaller på funksjonene fra klassen ArduinoSerial
arduino = ArduinoSerial()
#kaller på funksjonene fra klassen SoundPlayer
player = SoundPlayer()

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
        arduino.send_signal(hours, 0, 1)

    elif editAlarm == 2:
        if signal > 59:
            signal = 59
        minutes = signal
        minutes = f"{int(minutes):02}" # :02 gjør om tallet til to-siffra
        arduino.send_signal(minutes, 3, 1)

def volume_control(signal):
    if signal >= 100:
        volume_prosent = f"{signal}%"
    elif signal >= 10:
        volume_prosent = f" {signal}%"
    else:
        volume_prosent = f"  {signal}%"

    volume = signal/100
    player.set_volume(volume)
    arduino.send_signal(volume_prosent, 12, 1)

while True:
    databaseInfo = database.readInfoFromDatabase()  # Leser signal fra database
    if databaseInfo == 1:
        visit_mode = 1
        prev_vivit_mode = 0

    FrontendSignal = frontend.getInfoFromFrontend()  #Leser signal fra frontend
    if FrontendSignal is not None:
        if "LockDoorTime:" in FrontendSignal:

            externalDevices.lockdoor()
        elif FrontendSignal == "UnlockDoor":
            externalDevices.unlockdoor()
        elif FrontendSignal == "Falling Alarm":
            externalDevices.TurnOffFallingAlarm()

    ArduinoSignal = arduino.read_signal()  #Leser signal fra Arduino
    arduino.send_signal(getDateTime(), 0, 0)

    alarm_state = f"{hours}:{minutes}"
    if alarm_state == getTime():
        alarmTurnedOn = 1


    if ArduinoSignal is not None:
        if ArduinoSignal == "alarm_mode: 1":
            alarm_mode = 1

        elif ArduinoSignal == "alarm_mode: 0":
            alarm_mode = 0

        elif ArduinoSignal == "editAlarm_mode: 1":
            editAlarm_mode = 1

        elif ArduinoSignal == "editAlarm_mode: 2":
            editAlarm_mode = 2

        elif ArduinoSignal == "editAlarm_mode: 0":
            editAlarm_mode = 0

        elif ArduinoSignal == "visit_mode: 1":
            visit_mode = 1

        elif ArduinoSignal == "visit_mode: 0":
            visit_mode = 0

        elif alarm_time == 1 and editAlarm_mode != 0:
            update_alarm(ArduinoSignal)

        else:
            volume_control(ArduinoSignal)


    if alarm_mode == 1 and prev_alarm_mode != 1:
        arduino.send_signal("00:00", 0, 1)
        alarm_time = 1
    elif alarm_mode == 0 and prev_alarm_mode != 0:
        arduino.send_signal("     ", 0, 1)
        alarm_time = 0
    prev_alarm_mode = alarm_mode

    if editAlarm_mode == 1:
        editAlarm = 1
    elif editAlarm_mode == 2:
        editAlarm = 2
    elif editAlarm_mode == 0:
        editAlarm = 0

    if visit_mode == 1 and prev_vivit_mode != 1:
        database.sendInfoToDatabase("visit: 1")   #sende info til database
        visit_time = 1
    elif visit_mode == 0 and prev_vivit_mode != 0:
        database.sendInfoToDatabase("visit: 0")   #sende info til database
        visit_time = 0
    prev_vivit_mode = visit_mode

    if visit_mode == 1 and alarmTurnedOn == 0:
        arduino.send_signal("visit", 6, 1)
    elif visit_mode == 0:
        arduino.send_signal("      ", 6, 1)

    if alarmTurnedOn == 1 and alarm_mode == 1:
        if visit_mode == 1:
            arduino.send_signal("      ", 6, 1)

        alarmTimer += 1
        arduino.send_signal("Alarm!", 6, 1)
        if alarmTimer == 1:
            player.play_sound("alarm")

        if alarmTimer == 20 and visit_mode == 1:
            arduino.send_signal("visit ", 6, 1)
            player.stop_sound()   #skru av alarm lyd
            alarmTimer = 0
            alarmTurnedOn = 0

        if alarmTimer == 20:
            arduino.send_signal("      ", 6, 1)
            player.stop_sound()   #skru av alarm lyd
            alarmTimer = 0
            alarmTurnedOn = 0

    elif alarmTurnedOn == 1 and alarm_mode == 0:
        alarmTimer = 0
        alarmTurnedOn = 0
        player.stop_sound()       #skru av alarm lyd
        arduino.send_signal("      ", 6, 1)


    sleep(0.1)
