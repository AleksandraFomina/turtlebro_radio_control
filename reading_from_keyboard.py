import time
import serial
import keyboard

ser = serial.Serial()
ser.baudrate = 9600
ser.port = "/dev/ttyUSB0"
ser.dtr = False
ser.timeout = 0.5
ser.open()


ser.flushInput()



packet_size = 5 
data = '' 

def on_press(event):
    global data

    data += event.name

    if len(data) >= packet_size:
        
        ser.write(data.encode())
        
        data = ''
        time.sleep(1)

keyboard.on_press(on_press)
keyboard.wait()

    