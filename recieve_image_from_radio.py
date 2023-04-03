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

ser.flushInput()
img_encoded = bytes()

while 1 :
    img_encoded = ser.read(1024)
    #print(pack)
    if not img_encoded.find(b'\xff\xd8') == -1:
        #img_encoded += pack
        while img_encoded.find(b'\xff\xd9') == -1:
            #print("size:   ", len(img_encoded))
            img_encoded += ser.read(1024)
            #img_encoded += pack
            #time.sleep(0.5)
        image = cv2.imdecode(np.frombuffer(img_encoded, np.uint8), cv2.IMREAD_GRAYSCALE)
        #cv2.imwrite("photo.jpg", image)
        cv2.imshow("photo.jpg", image)
        cv2.waitKey(1000)
        img_encoded = bytes()
    #if cv2.waitKey(10) == 27:
    #    break
