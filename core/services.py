from core.entities import Alarm
from typing import Callable

# Tjenesteklasse for Headunit. Håndterer noe av logikken for Headunit.
class HeadunitService:
    def __init__(self, wireless_comm, arduino, sound_player, database):
        # Initialiser nødvendige komponenter
        self.wireless_comm = wireless_comm  # Trådløs kommunikasjonsadapter
        self.arduino = arduino  # Arduino-adapter
        self.sound_player = sound_player  # Lydspilleradapter
        self.database = database  # Databaseadapter

        # Initialiser status og attributter
        self.door_status = None  # Status for dør-lås (låst/ulåst)
        self.alarm = Alarm()  # Alarmobjekt
        self.edit_alarm = 0  # Alarm redigeringsstatus
        self.edit_alarm_mode = 0  # Redigeringsmodus for alarm
        self.alarm_time = 0  # Tidspunkt for alarm
        self.visit_mode = 0  # Besøksmodusstatus
        self.prev_alarm_mode = 0  # Forrige alarmmodus
        self.prev_visit_mode = 0  # Forrige besøksmodus
        

    def handle_door_lock_update(self, status: bool):
        # Oppdater status for dør-lås og utfør nødvendige handlinger.
        self.door_status = status
        if status:
            self.wireless_comm.lock_door()
        else:
            self.wireless_comm.unlock_door()

    def update_alarm(self, signal: int):
        # Oppdater alarmen basert på signal og redigeringsstatus.
        if self.edit_alarm == 1:
            signal = min(signal, 23)
            self.alarm.hours = f"{int(signal):02}"
            self.arduino.send_signal(self.alarm.hours, 0, 1)
        elif self.edit_alarm == 2:
            signal = min(signal, 59)
            self.alarm.minutes = f"{int(signal):02}"
            self.arduino.send_signal(self.alarm.minutes, 3, 1)

    def volume_control(self, signal: int):
        # Kontroller lydvolumet basert på signal.
        volume = min(max(signal, 0), 100) / 100
        volume_percent = f"{signal:3}%"
        self.sound_player.set_volume(volume)
        self.arduino.send_signal(volume_percent, 12, 1)