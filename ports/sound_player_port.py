from abc import ABC, abstractmethod

# SoundPlayerPort interface for å definere metoder for å kontrollere lydavspilling.
class SoundPlayerPort(ABC):
    @abstractmethod
    def set_volume(self, volume: float):
        pass

    @abstractmethod
    def play_sound(self, sound_name: str):
        pass

    @abstractmethod
    def pause_sound(self):
        pass

    @abstractmethod
    def play_alarm(self):
        pass

    @abstractmethod
    def stop_alarm(self):
        pass

    @abstractmethod
    def unpause_sound(self):
        pass