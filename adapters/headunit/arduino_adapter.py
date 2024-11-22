from ports.arduino_port import ArduinoPort
from adapters.headunit.headunit_arduino import ArduinoSerial

# Adapter for å kommunisere med Arduino via seriell kommunikasjon.
class ArduinoAdapter(ArduinoPort):
    def __init__(self, port, baudrate):
        self.arduino = ArduinoSerial(port=port, baudrate=baudrate)

    # Sender et signal til Arduino.
    def send_signal(self, message: str, position: int, flag: int):
        self.arduino.send_signal(message, position, flag)

    # Leser et signal fra Arduino.
    def read_signal(self) -> str:
        return self.arduino.read_signal()

    # Lukker tilkoblingen til Arduino.
    def close(self):
        #if hasattr(self.arduino, 'close'):
        self.arduino.close()
        
