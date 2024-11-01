import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0', 9600)
sleep(2)

def sendSignalToArduino(text, column, row):
    ser.write(b'C')
    ser.write(bytes([column]))

    ser.write(b'R')
    ser.write(bytes([row]))

    ser.write(b'T')
    ser.write(text.encode())

    ser.write(b'\n')
    sleep(0.1)