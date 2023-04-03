import serial
import time

ser = serial.Serial()
ser.baudrate = 9600
ser.port = "/dev/ttyUSB0"
ser.dtr = True
ser.timeout = 0.5
ser.open()


ser.flushInput()

ser.write(bytes.fromhex('AA FA 02'))
time.sleep(1)
response = ser.read(1024)
print(response)

ser.write(bytes.fromhex('AA FA 01'))
response = ser.read(1024)
print(response)
ser.write(bytes.fromhex('AA FA 03 14 01 05 07 05 02 01 01 00 00 00 00 00 00 0D 0A')) #39 channel (x27), 03 - speed 9600
response = ser.read(1024)
print(response)
ser.write(bytes.fromhex('AA FA 01'))
response = ser.read(1024)
print(response)

time.sleep(1)
ser.dtr = False
ser.close()


