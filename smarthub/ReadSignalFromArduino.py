import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

def readSignalFromArduino():
    read_serial = str(ser.readline())
    read_serial = read_serial.strip("b'").strip("\\r\\n")

    if "Encoder Position" in read_serial:
        read_serial = read_serial.replace("Encoder Position: ", "")
        read_serial = int(read_serial)

    return read_serial