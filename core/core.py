from adapters.headunit_wireless_communication import Wireless_communication
from adapters.headunit_arduino import ArduinoSerial
from adapters.database.headunit_db import Headunit
from adapters.sound_player import SoundPlayer
from time import sleep, strftime

# Knappe variabler
alarm_time = 0
visit_time = 0

# Alarm variabler
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

# reminder variabler
go_for_a_walk = ""
pill_dispensation = ""
eat_dinner = ""

# kaller på funksjonene fra klassen ArduinoSerial
arduino = ArduinoSerial()

# kaller på funksjonene fra klassen Wireless_communication
wireless = Wireless_communication()

# kaller på funksjonene fra klassen SoundPlayer
player = SoundPlayer()
player.set_volume(0.0)
player.play_sound("radio_simulering")

# kaller på funksjonene fra klassen SoundPlayer
db = Headunit()

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
        hours = f"{int(hours):02}"  # :02 gjør om tallet til to-siffra
        arduino.send_signal(hours, 0, 1)

    elif editAlarm == 2:
        if signal > 59:
            signal = 59
        minutes = signal
        minutes = f"{int(minutes):02}"  # :02 gjør om tallet til to-siffra
        arduino.send_signal(minutes, 3, 1)


def volume_control(signal):
    if signal >= 100:
        volume_prosent = f"{signal}%"
    elif signal >= 10:
        volume_prosent = f" {signal}%"
    else:
        volume_prosent = f"  {signal}%"

    volume = signal / 100
    player.set_volume(volume)
    arduino.send_signal(volume_prosent, 12, 1)

def reminder():
    if pill_dispensationTime == getTime():
        wireless.pillDispensation()
    elif go_for_a_walk == getTime():
        player.play_sound("go_for_a_walk")
        db.updateReminder("go_for_a_walk")
    elif eat_dinner == getTime():
        player.play_sound("eat_dinner")
        db.updateReminder("eat_dinner")


while True:
    # Leser fra database
    visit_mode = db.readInfoFromDatabase("visit")
    doorlock = db.readInfoFromDatabase("doorlock")
    if doorlock == 1:
        wireless.lockDoor()
    elif doorlock == 0:
        wireless.unlockDoor()
    pillDispensation = db.readInfoFromDatabase("pillDispensation")
    if pillDispensation == getTime():
        wireless.pillDispensation()

    if db.reminder()[pill_dispensation] != "":
        pill_dispensationTime = db.reminder()[pill_dispensation]

    if db.reminder()[go_for_a_walk] != "":
        go_for_a_walk = db.reminder()[go_for_a_walk]

    if db.reminder()[eat_dinner] != "":
        eat_dinner = db.reminder()[eat_dinner]

    if

    # Leser signal fra ESP32 og sender til database
    info = wireless.readSignalFromESP32()
    if "door_is_locked" in info:
        db.sendInfoToDatabase("doorlock", 1)
    elif "door_is_unlocked" in info:
        db.sendInfoToDatabase("doorlock", 0)
    if "fall_detected" in info:
        db.sendInfoToDatabase("fall_sensor", 1)
    elif "false_alarm" in info:
        db.sendInfoToDatabase("fall_sensor", 0)
    if "pills_dispensed" in info:
        db.sendPillsDropedToDatabase("pillDispensation", 1, getTime())

    # Leser signal fra Arduino
    signal = arduino.read_signal()
    arduino.send_signal(getDateTime(), 0, 0)

    alarm_state = f"{hours}:{minutes}"
    if alarm_state == getTime() and editAlarm_mode == 0:
        alarmTurnedOn = 1
    print(signal)

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

    if go_for_a_walk == getTime():
        player.play_sound("go_for_a_walk")
        db.updateReminder("go_for_a_walk")

    if pill_dispensation == getTime():
        player.play_sound("pill_dispensation")
        db.updateReminder("pill_dispensation")

    if eat_dinner == getTime():
        player.play_sound("eat_dinner")
        db.updateReminder("eat_dinner")

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
        # sende info til database
        db.sendInfoToDatabase("visit", 1)
        player.pause_sound()
        visit_time = 1
    elif visit_mode == 0 and prev_vivit_mode != 0:
        # sende info til database
        db.sendInfoToDatabase("visit", 0)
        player.unpause_sound()
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
            player.pause_sound()
            #player.play_sound("alarm")
            player.play_alarm()

        if alarmTimer == 5 and visit_mode == 1:
            arduino.send_signal("visit ", 6, 1)
            player.stop_alarm()     # skru av alarm lyd
            player.unpause_sound()
            alarmTimer = 0
            alarmTurnedOn = 0

        if alarmTimer == 5:
            arduino.send_signal("      ", 6, 1)
            player.stop_alarm()    # skru av alarm lyd
            player.unpause_sound()
            alarmTimer = 0
            alarmTurnedOn = 0

    elif alarmTurnedOn == 1 and alarm_mode == 0:
        arduino.send_signal("      ", 6, 1)
        player.stop_alarm()  # skru av alarm lyd
        player.unpause_sound()
        alarmTimer = 0
        alarmTurnedOn = 0

    sleep(0.1)
