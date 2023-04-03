import rospy
import cv2
import numpy as np
from sensor_msgs.msg import CompressedImage
import serial
import time


class ImageSender():
        def __init__(self):
                
                self.sub = rospy.Subscriber("/front_camera/image_raw/compressed", CompressedImage, self.cb_video_capture)
                self.image_from_ros_camera = []
                rospy.init_node("image_sender")
                

        def cb_video_capture(self, image_msg):
                 
                scale_percent = 50
                
                np_arr = np.frombuffer(image_msg.data, np.uint8)
                self.image_from_ros_camera = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
                
                width = int(self.image_from_ros_camera.shape[1] * scale_percent / 100)
                height = int(self.image_from_ros_camera.shape[0] * scale_percent / 100)
                dsize = (width, height)

                self.image_from_ros_camera = cv2.resize(self.image_from_ros_camera, dsize)

def img_to_arr(img):
        quality = 10
        _, img_encoded = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, quality])

        return img_encoded
        
def send(img, pack_size, ser):
        pack_size = pack_size
        #img_encoded = img 
        pack = img.tobytes()
        
        pack_num  = int((len(pack))/pack_size)+1

        for i in range(0, pack_num):
                serial_pack = pack[i*pack_size:(i+1)*pack_size]
                send_bytes = ser.write(serial_pack)
                rospy.loginfo("Send data pack %i: %s size 0f message:%i", i, send_bytes, len(pack))
                time.sleep(1)

if __name__ =="__main__":
        ser = serial.Serial()
        ser.baudrate = 9600
        ser.port = "/dev/ttyUSB0"
        ser.dtr = False
        ser.timeout = 0.5
        ser.open()
        ser.flushInput()

        sender = ImageSender()
        pack_size = 1024
        while not rospy.is_shutdown():
                img = img_to_arr(sender.image_from_ros_camera)
                send(img, pack_size, ser)
                #rospy.sleep(0.1)



