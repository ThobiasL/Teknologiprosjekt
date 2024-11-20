from adapters.headunit_wireless_communication import Wireless_communication
from adapters.headunit_arduino import ArduinoSerial
from services.headunit import Headunit
from adapters.sound_player import SoundPlayer
from time import sleep, strftime
from application.database_core import SessionLocal
from services.periodic_reader import PeriodicDatabaseReader

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
prev_visit_mode = -1

# Pille dispenser variabler


# Kall på funksjonene fra ArduinoSerial
arduino = ArduinoSerial()

# Kall på funksjonene fra Wireless_communication
wireless = Wireless_communication()

# Kall på funksjonene fra SoundPlayer
player = SoundPlayer()
player.set_volume(0.1)
player.play_sound("radio_simulering")
taskPlaying = False

# Opprett database sessions og klasser
main_session = SessionLocal()  # Hovedtrådens session
db = Headunit(main_session)

def handle_door_lock_update(status):
    try:
        if status:
            wireless.lockDoor()
        else:
            wireless.unlockDoor()
    except Exception:
        pass  # Ignorer unntak her for stabilitet

# Opprett PeriodicDatabaseReader
db_reader = PeriodicDatabaseReader(SessionLocal, on_door_lock_update=handle_door_lock_update, interval=0.5)
db_reader.start()

def getDateTime():
    return strftime("%d.%m.%Y %H:%M")

def getTime():
    return strftime("%H:%M:%S")

def update_alarm(signal):
    global hours, minutes

    if editAlarm == 1:
        if signal > 23:
            signal = 23
        hours = f"{int(signal):02}"  # Formater som to-sifret
        arduino.send_signal(hours, 0, 1)

    elif editAlarm == 2:
        if signal > 59:
            signal = 59
        minutes = f"{int(signal):02}"  # Formater som to-sifret
        arduino.send_signal(minutes, 3, 1)

def volume_control(signal):
    volume = min(max(signal, 0), 100) / 100  # Sikre at volumet er mellom 0 og 100
    volume_prosent = f"{signal:3}%"  # Formater med riktig plassering
    player.set_volume(volume)
    arduino.send_signal(volume_prosent, 12, 1)

# Hovedløkken
try:
    while True:
        # Behandle trådløs kommunikasjon
        wireless_info = wireless.getMessage()

        if wireless_info:
            if "door_is_locked" in wireless_info:
                db.sendAutoDoorLockTimeToDatabase(1)
            elif "door_is_unlocked" in wireless_info:
                db.sendAutoDoorLockTimeToDatabase(0)
            elif "fall_detected" in wireless_info:
                print("Fall detected")
            elif "false_alarm" in wireless_info:
                print("False alarm")
            elif "Pills_Dispens" in wireless_info:
                print("Pills_Dispens")

        # Håndtere dør-lås basert på databaseverdier        
            
        doorlock = db.readVariableStatusFromDatabase()
        doorlockTime = db.readAutoDoorLockTimeFromDatabase()
        doorlockTime = f"{doorlockTime}:00"

        if doorlockTime == getTime():
            wireless.unlockDoor()
    
        # Håndtere medisinering
        # Hent dagens navn
        today = strftime("%A")
        
        # Hent medisin-doser fra databasen
        doses = db.readMedicationDosesFromDatabase(today)

        if not doses:
            print(f"Ingen doser planlagt for {today}.")      


        # Gå gjennom dosene for å håndtere doser som skal gis
        for dose_key, is_scheduled in doses.items():
            if is_scheduled and dose_key.startswith("scheduled"):
                dose_id = int(dose_key.split("_")[-1])
                scheduled_time = doses.get(f"dose_{dose_id}")
                scheduled_time = str(scheduled_time) + ":00"

                # Sjekk om tidspunktet matcher nåværende tid
                if scheduled_time == getTime():
                    wireless.pillDispensation()
                    print(f"Dose {dose_id} sendt til pille-dispenseren.")
                    # player.pause_sound()
                    # player.play_sound("medication")

        # Håndtere signalet for å markere dosen som tatt
        if wireless_info == "Pills_Dispens":
            for dose_key, is_scheduled in doses.items():
                if is_scheduled and dose_key.startswith("scheduled"):
                    dose_id = int(dose_key.split("_")[-1])
                    medication_id = doses.get("medication_id")

                    try:
                        #db.sendMedicationDosesStatusToDatabase(medication_id, dose_id)
                        print(f"Medisin-dose {dose_id} markert som tatt!")
                    except Exception as e:
                        print(f"Feil under oppdatering av status for dose {dose_id}: {e}")

            
        
        # Håndtere oppgaver
        tasks = db.readTasksFromDatabase()
        for task in tasks:
            taskTime = f"{task['time']}:00"
            if taskTime == getTime():
                if task["name"] == "go_for_a_walk":
                    player.pause_sound()
                    player.play_sound("go_for_a_walk")
                    db.taskDone(task["name"], task["time"])
                elif task["name"] == "eat_dinner":
                    player.pause_sound()
                    player.play_sound("eat_dinner")
                    db.taskDone(task["name"], task["time"])

        # Leser signaler fra Arduino
        signal = arduino.read_signal()
        arduino.send_signal(getDateTime(), 0, 0)

        alarm_state = f"{hours}:{minutes}:00"
        if alarm_state == getTime() and editAlarm_mode == 0:
            alarmTurnedOn = 1

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

        if visit_mode == 1 and prev_visit_mode != 1:
            #sende info til database
            visit_time = 1
        elif visit_mode == 0 and prev_visit_mode != 0:
            #sende info til database
            visit_time = 0
        prev_visit_mode = visit_mode

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
                

            if alarmTimer == 12 and visit_mode == 1:
                arduino.send_signal("visit ", 6, 1)
                player.stop_alarm()   #skru av alarm lyd
            #   sleep(0.5)
                player.unpause_sound()
                alarmTimer = 0
                alarmTurnedOn = 0

            if alarmTimer == 12:
                arduino.send_signal("      ", 6, 1)
                player.stop_alarm()   #skru av alarm lyd
                #sleep(0.5)
                player.unpause_sound()
                alarmTimer = 0
                alarmTurnedOn = 0

        elif alarmTurnedOn == 1 and alarm_mode == 0:
            #alarm_state = "01:10"
            arduino.send_signal("      ", 6, 1)
            player.stop_alarm()       #skru av alarm lyd
            #sleep(0.5)
            player.unpause_sound()
            #sleep(0.2)
            alarmTimer = 0
            alarmTurnedOn = None

        sleep(0.1)
finally:
    if wireless:
        wireless.close_sockets()
    if main_session:
        main_session.close()
    if db_reader:
        db_reader.stop()
