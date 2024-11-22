from ports.wireless_communication_port import WirelessCommunicationPort
from adapters.headunit.headunit_wireless_communication import Wireless_communication

# Adapter for å kommunisere med ESP32 via trådløs kommunikasjon. Implementerer WirelessCommunicationPort-interfacet.
# Inkluderer funktioner for å låse og låse opp dør, motta meldinger og dispensere piller.
class WirelessCommunicationAdapter(WirelessCommunicationPort):
    def __init__(self):
        self.wireless = Wireless_communication()

    def lock_door(self):
        self.wireless.lockDoor()

    def unlock_door(self):
        self.wireless.unlockDoor()

    def get_message(self) -> str:
        return self.wireless.getMessage()

    def pill_dispensation(self):
        self.wireless.pillDispensation()

    def close(self):
        self.wireless.close_sockets()
