import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    read_serial = str(ser.readline())
    read_serial = read_serial.strip("b'").strip("\\r\\n")

    if "Enconder Position" in read_serial:
        read_serial = read_serial.replace("Encoder Postion: ", "")
        read_serial = int(read_serial)

    readSignal = read_serial