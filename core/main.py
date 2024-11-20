import sys
import os

# Fjern eventuelle feilaktige søkestier
if "/home/teknologi-prosjekt/GitHub/Teknologiprosjekt/core" in sys.path:
    sys.path.remove("/home/teknologi-prosjekt/GitHub/Teknologiprosjekt/core")

# Legg til prosjektroten i sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)
import traceback
from time import sleep, strftime
from core.services import HeadunitService
from core.models.datetime_model import DateTimeModel
from adapters.wireless_communication_adapter import WirelessCommunicationAdapter
from adapters.arduino_adapter import ArduinoAdapter
from adapters.sound_player_adapter import SoundPlayerAdapter
from adapters.database_adapter import DatabaseAdapter
from services.periodic_reader2 import PeriodicDatabaseReader


def main():
    # Initialize adapters
    wireless_adapter = WirelessCommunicationAdapter()
    arduino_adapter = ArduinoAdapter()
    sound_player_adapter = SoundPlayerAdapter()
    database_adapter = DatabaseAdapter()

    # Initialize datetime
    current_datetime = DateTimeModel.get_datetime()
    current_time = DateTimeModel.get_time()

    # Initialize service
    headunit_service = HeadunitService(
        wireless_comm=wireless_adapter,
        arduino=arduino_adapter,
        sound_player=sound_player_adapter,
        database=database_adapter
    )


    # Define handler for door lock updates
    def handle_door_lock_update(status: bool):
        headunit_service.handle_door_lock_update(status)

    # Initialize and start PeriodicDatabaseReader
    db_reader = PeriodicDatabaseReader(
        db_session_factory=database_adapter.get_session_factory(),
        on_door_lock_update=handle_door_lock_update,
        interval=0.5
    )
    db_reader.start()

    try:
        while True:
            # Behandle trådløs kommunikasjon
            wireless_info = wireless_adapter.get_message()

            if wireless_info:
                if "door_is_locked" in wireless_info:
                    database_adapter.send_auto_door_lock_time(1)
                elif "door_is_unlocked" in wireless_info:
                    database_adapter.send_auto_door_lock_time(0)
                elif "fall_detected" in wireless_info:
                    print("Fall detected")
                elif "false_alarm" in wireless_info:
                    print("False alarm")
                elif "Pills_Dispens" in wireless_info:
                    print("Pills_Dispens")

            # Håndtere dør-lås basert på databaseverdier        
            doorlock_time = database_adapter.read_auto_door_lock_time()

            if doorlock_time == current_time:
                wireless_adapter.unlock_door()

            # Håndtere medisinering
            today = strftime("%A")
            doses = database_adapter.read_medication_doses(today)

            if not doses:
                print(f"Ingen doser planlagt for {today}.")

            for dose_key, is_scheduled in doses.items():
                if is_scheduled and dose_key.startswith("scheduled"):
                    dose_id = int(dose_key.split("_")[-1])
                    scheduled_time = f"{doses.get(f'dose_{dose_id}')}:00"

                    if scheduled_time == current_time:
                        wireless_adapter.pill_dispensation()
                        print(f"Dose {dose_id} sendt til pille-dispenseren.")
                        # sound_player_adapter.pause_sound()
                        # sound_player_adapter.play_sound("medication")

            # Håndtere signalet for å markere dosen som tatt
            if wireless_info == "Pills_Dispens":
                for dose_key, is_scheduled in doses.items():
                    if is_scheduled and dose_key.startswith("scheduled"):
                        dose_id = int(dose_key.split("_")[-1])
                        medication_id = doses.get("medication_id")

                        try:
                            # database_adapter.send_medication_dose_status(medication_id, dose_id)
                            print(f"Medisin-dose {dose_id} markert som tatt!")
                        except Exception as e:
                            print(f"Feil under oppdatering av status for dose {dose_id}: {e}")

            # Håndtere oppgaver
            tasks = database_adapter.read_tasks()
            for task in tasks:
                task_time = f"{task['time']}:00"
                if task_time == current_time:
                    if task["name"] == "go_for_a_walk":
                        sound_player_adapter.pause_sound()
                        sound_player_adapter.play_sound("go_for_a_walk")
                        database_adapter.task_done(task["name"], task["time"])
                    elif task["name"] == "eat_dinner":
                        sound_player_adapter.pause_sound()
                        sound_player_adapter.play_sound("eat_dinner")
                        database_adapter.task_done(task["name"], task["time"])

            # Leser signaler fra Arduino
            signal = arduino_adapter.read_signal()
            arduino_adapter.send_signal(current_datetime, 0, 0)

            # Oppdatere alarm
            headunit_service.alarm.state = f"{headunit_service.alarm.hours}:{headunit_service.alarm.minutes}:00"
            if headunit_service.alarm.state == current_time and headunit_service.alarm.edit_alarm_mode == 0:
                headunit_service.alarm.turned_on = True

            if signal:
                # Prosesser signaler
                if signal.startswith("alarm_mode:"):
                    _, value = signal.split(":")
                    headunit_service.alarm.mode = int(value.strip())
                elif signal.startswith("editAlarm_mode:"):
                    _, value = signal.split(":")
                    headunit_service.edit_alarm_mode = int(value.strip())
                elif signal.startswith("visit_mode:"):
                    _, value = signal.split(":")
                    headunit_service.visit_mode = int(value.strip())
                elif headunit_service.alarm_time == 1 and headunit_service.edit_alarm_mode != 0:
                    headunit_service.update_alarm(int(signal))
                else:
                    headunit_service.volume_control(int(signal))

            # Håndtere alarm logikk
            if headunit_service.alarm.mode == 1 and headunit_service.prev_alarm_mode != 1:
                arduino_adapter.send_signal("00:00", 0, 1)
                headunit_service.alarm_time = 1
            elif headunit_service.alarm.mode == 0 and headunit_service.prev_alarm_mode != 0:
                arduino_adapter.send_signal("     ", 0, 1)
                headunit_service.alarm_time = 0
            headunit_service.prev_alarm_mode = headunit_service.alarm.mode

            # Oppdater editAlarm basert på editAlarm_mode
            headunit_service.edit_alarm = headunit_service.edit_alarm_mode

            # Oppdater visit_mode
            if headunit_service.visit_mode == 1 and headunit_service.prev_visit_mode != 1:
                # Send info til database
                headunit_service.visit_time = 1
            elif headunit_service.visit_mode == 0 and headunit_service.prev_visit_mode != 0:
                # Send info til database
                headunit_service.visit_time = 0
            headunit_service.prev_visit_mode = headunit_service.visit_mode

            if headunit_service.visit_mode == 1 and not headunit_service.alarm.turned_on:
                arduino_adapter.send_signal("visit", 6, 1)
            elif headunit_service.visit_mode == 0:
                arduino_adapter.send_signal("      ", 6, 1)

            if headunit_service.alarm.turned_on and headunit_service.alarm.mode == 1:
                if headunit_service.visit_mode == 1:
                    arduino_adapter.send_signal("      ", 6, 1)

                headunit_service.alarm.timer += 1
                arduino_adapter.send_signal("Alarm!", 6, 1)
                if headunit_service.alarm.timer == 1:
                    sound_player_adapter.pause_sound()
                    sound_player_adapter.play_alarm()

                if headunit_service.alarm.timer == 12 and headunit_service.visit_mode == 1:
                    arduino_adapter.send_signal("visit ", 6, 1)
                    sound_player_adapter.stop_alarm()
                    sound_player_adapter.unpause_sound()
                    headunit_service.alarm.timer = 0
                    headunit_service.alarm.turned_on = False

                if headunit_service.alarm.timer == 12:
                    arduino_adapter.send_signal("      ", 6, 1)
                    sound_player_adapter.stop_alarm()
                    sound_player_adapter.unpause_sound()
                    headunit_service.alarm.timer = 0
                    headunit_service.alarm.turned_on = False

            elif headunit_service.alarm.turned_on and headunit_service.alarm.mode == 0:
                arduino_adapter.send_signal("      ", 6, 1)
                sound_player_adapter.stop_alarm()
                sound_player_adapter.unpause_sound()
                headunit_service.alarm.timer = 0
                headunit_service.alarm.turned_on = None

            sleep(0.1)
    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        traceback.print_exc()
    finally:
        # Lukk alle adaptere
        wireless_adapter.close()
        arduino_adapter.close()
        sound_player_adapter.close()
        database_adapter.close()
        db_reader.stop()

if __name__ == "__main__":
    main()
