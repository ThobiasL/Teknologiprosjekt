from core.entities import Alarm
from typing import Callable

class HeadunitService:
    def __init__(self, wireless_comm, arduino, sound_player, database):
        self.wireless_comm = wireless_comm
        self.arduino = arduino
        self.sound_player = sound_player
        self.database = database
        self.alarm = Alarm()
        self.edit_alarm = 0
        self.edit_alarm_mode = 0
        self.alarm_time = 0
        self.visit_mode = 0
        self.prev_alarm_mode = 0 
        self.prev_visit_mode = 0 
        

    def handle_door_lock_update(self, status: bool):
        if status:
            self.wireless_comm.lock_door()
        else:
            self.wireless_comm.unlock_door()

    def update_alarm(self, signal: int):
        if self.edit_alarm == 1:
            signal = min(signal, 23)
            self.alarm.hours = f"{int(signal):02}"
            self.arduino.send_signal(self.alarm.hours, 0, 1)
        elif self.edit_alarm == 2:
            signal = min(signal, 59)
            self.alarm.minutes = f"{int(signal):02}"
            self.arduino.send_signal(self.alarm.minutes, 3, 1)

    def volume_control(self, signal: int):
        volume = min(max(signal, 0), 100) / 100
        volume_percent = f"{signal:3}%"
        self.sound_player.set_volume(volume)
        self.arduino.send_signal(volume_percent, 12, 1)