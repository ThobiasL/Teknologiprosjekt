from abc import ABC, abstractmethod

# ArduinoPort-grensesnittet som definerer metoder for å sende og lese signaler fra Arduino.
class ArduinoPort(ABC):
    @abstractmethod
    def send_signal(self, message: str, position: int, flag: int):
        pass

    @abstractmethod
    def read_signal(self) -> str:
        pass