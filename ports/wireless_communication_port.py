from abc import ABC, abstractmethod

# WirelessCommunicationPort interface for å definere metoder for å kommunisere med ESP.
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