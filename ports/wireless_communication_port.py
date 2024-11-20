from abc import ABC, abstractmethod

class WirelessCommunicationPort(ABC):
    @abstractmethod
    def lock_door(self):
        pass

    @abstractmethod
    def unlock_door(self):
        pass

    @abstractmethod
    def get_message(self) -> str:
        pass

    @abstractmethod
    def pill_dispensation(self):
        pass