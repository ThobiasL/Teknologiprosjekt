import serial
from time import sleep

# Klasse for å kommunisere med Arduino via serieport. 
# Inkluderer funksjoner for å sende og motta signaler, samt lukke tilkoblingen.
class ArduinoSerial:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, read_delay=0.1, write_delay=0.1):
        self.ser = serial.Serial(port, baudrate)
        sleep(read_delay)  # Venter på at serial skal initialisere
        self.write_delay = write_delay

    # Leser signal fra Arduino.
    def read_signal(self):
        #Leser et signal fra Arduino. Hvis 'Encoder Position' er i svaret, trekker ut posisjonen som et heltall.
        if self.ser.in_waiting > 0:
            read_serial = str(self.ser.readline())
            read_serial = read_serial.strip("b'").strip("\\r\\n")

            if "Encoder Position" in read_serial:
                read_serial = read_serial.replace("Encoder Position: ", "")
                read_serial = int(read_serial)
            return read_serial
        return None

    # Sender et formatert signal til Arduino med spesifiserte tekst-, kolonne- og radverdier.
    def send_signal(self, text, column, row):
        self.ser.write(b'C')
        self.ser.write(bytes([column]))

        self.ser.write(b'R')
        self.ser.write(bytes([row]))

        self.ser.write(b'T')
        self.ser.write(text.encode())

        self.ser.write(b'\n')
        sleep(self.write_delay)

    # Lukker tilkoblingen til Arduino.
    def close(self):
        if self.ser.is_open:
            self.ser.close()
        #if hasattr(self.connection, 'is_open') and self.connection.is_open:
            #self.connection.close()