import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)

def sendSignalToArduino(text, column, row):
    ser.write(text.encode())
    ser.write(column.encode())
    ser.write(row.encode())
    time.sleep(0.1)

def clearLCD():
    ser.write("clear".encode())
    time.sleep(0.1)