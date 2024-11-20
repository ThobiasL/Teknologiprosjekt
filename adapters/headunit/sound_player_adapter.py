from ports.sound_player_port import SoundPlayerPort
from adapters.headunit.sound_player import SoundPlayer

class SoundPlayerAdapter(SoundPlayerPort):
    def __init__(self):
        self.player = SoundPlayer()
        self.player.set_volume(0.1)
        self.player.play_sound("radio_simulering")
        self.task_playing = False

    def set_volume(self, volume: float):
        self.player.set_volume(volume)

    def play_sound(self, sound_name: str):
        self.player.play_sound(sound_name)

    def pause_sound(self):
        self.player.pause_sound()

    def play_alarm(self):
        self.player.play_alarm()

    def stop_alarm(self):
        self.player.stop_alarm()

    def unpause_sound(self):
        self.player.unpause_sound()

    def close(self):
        self.player.stop()