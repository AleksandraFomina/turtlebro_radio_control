import serial
import time

ser = serial.Serial()
ser.baudrate = 9600
ser.port = "/dev/ttyUSB0"
ser.dtr = False
ser.timeout = 0.5
ser.open()

ser.flushInput()

while True:
    mess = input()
    ser.write(mess.encode())
        
    time.sleep(1)