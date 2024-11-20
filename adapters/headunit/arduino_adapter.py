from ports.arduino_port import ArduinoPort
from adapters.headunit.headunit_arduino import ArduinoSerial

class ArduinoAdapter(ArduinoPort):
    def __init__(self):
        self.arduino = ArduinoSerial()

    def send_signal(self, message: str, position: int, flag: int):
        self.arduino.send_signal(message, position, flag)

    def read_signal(self) -> str:
        return self.arduino.read_signal()

    def close(self):
        self.arduino.close()
