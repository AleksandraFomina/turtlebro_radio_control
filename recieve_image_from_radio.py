import serial
import cv2
import numpy as np
import time


ser = serial.Serial()
ser.baudrate = 9600
ser.port = "/dev/ttyUSB0"
ser.dtr = False
ser.timeout = 0.5
ser.open()
sum = 0
flag =0
ser.flushInput()
img_encoded = bytearray()

while flag == 0:
    pack = ser.read(2)
    #print("pack ",pack)
    pack_size = int.from_bytes(pack, "big")
    #print("size ",pack_size)
    if pack_size>0:
        pack = ser.read(1024)
        while 1:
            sum += len(pack)
            #print("sum:   ", sum)
            img_encoded += bytearray(pack)
            pack = ser.read(1024)
            if sum>=pack_size:
                flag = 1
                break
            time.sleep(0.5)

#print('len img: ', len(img_encoded))
#print(img_encoded)
np_arr = np.frombuffer(img_encoded, np.uint8)
image = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
cv2.imwrite("photo.jpg", image)
#print('ok')
