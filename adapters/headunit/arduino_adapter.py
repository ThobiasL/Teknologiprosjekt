from ports.arduino_port import ArduinoPort
from adapters.headunit.headunit_arduino import ArduinoSerial

class ArduinoAdapter(ArduinoPort):
    def __init__(self, port, baudrate):
        self.arduino = ArduinoSerial(port=port, baudrate=baudrate)

    def send_signal(self, message: str, position: int, flag: int):
        self.arduino.send_signal(message, position, flag)

    def read_signal(self) -> str:
        return self.arduino.read_signal()

    def close(self):
        #if hasattr(self.arduino, 'close'):
        self.arduino.close()
        
