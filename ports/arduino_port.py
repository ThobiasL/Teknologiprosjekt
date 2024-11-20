from abc import ABC, abstractmethod

class ArduinoPort(ABC):
    @abstractmethod
    def send_signal(self, message: str, position: int, flag: int):
        pass

    @abstractmethod
    def read_signal(self) -> str:
        pass