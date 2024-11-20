import serial
from time import sleep

class ArduinoSerial:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, read_delay=0.1, write_delay=0.1):
        self.ser = serial.Serial(port, baudrate)
        sleep(read_delay)  # Delay to allow Arduino to initialize
        self.write_delay = write_delay

    def read_signal(self):
        """Reads a signal from the Arduino. If 'Encoder Position' is in the response, extracts the position as an integer."""
        if self.ser.in_waiting > 0:
            read_serial = str(self.ser.readline())
            read_serial = read_serial.strip("b'").strip("\\r\\n")

            if "Encoder Position" in read_serial:
                read_serial = read_serial.replace("Encoder Position: ", "")
                read_serial = int(read_serial)
            return read_serial
        return None

    def send_signal(self, text, column, row):
        """Sends a formatted signal to the Arduino with specified text, column, and row values."""
        self.ser.write(b'C')
        self.ser.write(bytes([column]))

        self.ser.write(b'R')
        self.ser.write(bytes([row]))

        self.ser.write(b'T')
        self.ser.write(text.encode())

        self.ser.write(b'\n')
        sleep(self.write_delay)

    def close(self):
        if self.connection.is_open:
            self.connection.close()