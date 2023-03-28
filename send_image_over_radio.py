import rospy
import cv2
import numpy as np
from sensor_msgs.msg import CompressedImage
import serial
import time


rospy.init_node("image_sender")

ser = serial.Serial()
ser.baudrate = 9600
ser.port = "/dev/ttyUSB0"
ser.dtr = False
ser.timeout = 0.5
ser.open()


ser.flushInput()

def cb_video_capture(image_msg):
        global image_from_ros_camera
        scale_percent = 50
        
        np_arr = np.frombuffer(image_msg.data, np.uint8)
        image_from_ros_camera = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        
        width = int(image_from_ros_camera.shape[1] * scale_percent / 100)
        height = int(image_from_ros_camera.shape[0] * scale_percent / 100)
        # dsize
        dsize = (width, height)

        # resize image
        image_from_ros_camera = cv2.resize(image_from_ros_camera, dsize)

def img_to_arr(img):
        quality = 20
        _, img_encoded = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, quality])

        return img_encoded


rospy.Subscriber("/front_camera/image_raw/compressed", CompressedImage, cb_video_capture)
rospy.sleep(1)



pack_size = 255
img_encoded = img_to_arr(image_from_ros_camera)
pack = img_encoded.tobytes()
#print("img:  ", img_encoded)

#print("pack ", pack)  
pack_num  = int((len(pack))/pack_size)+1
#print("num ", pack_num, "len ", len(pack))
#print("len ", (len(pack)).to_bytes(2, "big"))

ser.write((len(pack)).to_bytes(2, "big"))
time.sleep(1)
for i in range(0, pack_num):
        serial_pack = pack[i*pack_size:(i+1)*pack_size]
        send_bytes = ser.write(serial_pack)
        rospy.loginfo("Send data pack %i: %s", i, send_bytes)
        time.sleep(3)