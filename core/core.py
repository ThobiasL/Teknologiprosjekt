from adapters.headunit_wireless_communication import Wireless_communication
from adapters.headunit_arduino import ArduinoSerial
from services.headunit import Headunit
from adapters.sound_player import SoundPlayer
from time import sleep, strftime
from application.database_core import SessionLocal

# Knappe variabler
alarm_time = 0
visit_time = 0

# Alarm variabler
hours = "00"
minutes = "00"
alarm_mode = 0
alarm_state = f"{hours}:{minutes}:00"
alarmTurnedOn = 0
alarmTimer = 0
prev_alarm_mode = -1

editAlarm = 0
editAlarm_mode = 0

visit_mode = 0
prev_vivit_mode = -1

# kaller på funksjonene fra klassen ArduinoSerial
arduino = ArduinoSerial()

# kaller på funksjonene fra klassen Wireless_communication
wireless = Wireless_communication()

# kaller på funksjonene fra klassen SoundPlayer
player = SoundPlayer()
player.set_volume(0.1)
player.play_sound("radio_simulering")
taskPlaying = False

db_session = SessionLocal()

db = Headunit(db_session)

def getDateTime():
    return strftime("%d.%m.%Y %H:%M")


def getTime():
    return strftime("%H:%M:%S")


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

wireless.pillDispensation()
while True:
    # Leser fra database
    #visit_mode = db.readVisteStatusFromDatabase()
    doorlock = db.readVariableStatusFromDatabase()
    doorlockTime = db.readAutoDoorLockTimeFromDatabase()
    tasks = db.readTasksFromDatabase()
    #wireless.readSignalFromESP32()
    
    
    # Leser signal fra ESP32 og sender til database
    wireless_info = wireless.getMessage()
    
    if wireless_info is not None:
        if "door_is_locked" in wireless_info:
            db.sendAutoDoorLockTimeToDatabase(1)
        if "door_is_unlocked" in wireless_info:
            db.sendAutoDoorLockTimeToDatabase(0)
        if "fall_detected" in wireless_info:
            print("Fall detected")
            # 1 sende info til database
        if "false_alarm" in wireless_info:
            print("False alarm")
            # 0 sende info til database
        if "Pills_Dispens" in wireless_info:
            print("Pills_Dispens")
            #db.sendMedicationDosesStatusToDatabase()

    doorlockTime = str(doorlockTime) + ":00"
    if doorlockTime == getTime():
        if doorlock:
            wireless.lockDoor()
        if doorlock:
            wireless.unlockDoor()

    '''
    Today = strftime("%A")  # sjekker hvilken ukedag det er i dag
    Doses = db.readMedicationDosesFromDatabase(Today)
    #for i in range(1, 5):
        #if Doses[f"time_{i}"] == getTime():
            #wireless.pillDispensation()
            #player.pause_sound()
            #player.play_sound("pill_dispensation")   # planlagt vidre utvikling

    tasksTime = tasks["time"] + ":00"
    if tasksTime == getTime():
        if tasks["name"] == "go_for_a_walk":
            player.pause_sound()
            player.play_go_for_a_walk()
            db.taskDone("go_for_a_walk", tasks["time"])
        elif tasks["name"] == "eat_dinner":
            player.pause_sound()
            player.play_eat_dinner()
            db.taskDone("eat_dinner", tasks["time"])
        taskPlaying = True
        x = 0
    if taskPlaying:
        x += 1
        if x == 5:
            player.stop_eat_dinner()
            player.stop_go_for_a_walk()
            player.unpause_sound()
            taskPlaying = False
    '''

    # Leser signal fra Arduino
    signal = arduino.read_signal()
    arduino.send_signal(getDateTime(), 0, 0)

    alarm_state = f"{hours}:{minutes}:00"
    if alarm_state == getTime() and editAlarm_mode == 0:
        alarmTurnedOn = 1


    if signal is not None:
        print(signal)
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
        #db.sendVisteStatusToDatabase(True)
        visit_time = 1
    elif visit_mode == 0 and prev_vivit_mode != 0:
        # sende info til database
        #db.sendVisteStatusToDatabase(False)
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
