import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0', 9600)
sleep(0.1)

def readSignalFromArduino():
    if ser.in_waiting > 0:
        read_serial = str(ser.readline())
        read_serial = read_serial.strip("b'").strip("\\r\\n")

        if "Encoder Position" in read_serial:
            read_serial = read_serial.replace("Encoder Position: ", "")
            read_serial = int(read_serial)

        return read_serial
    return None