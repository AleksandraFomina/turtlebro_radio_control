import rospy
import serial
from geometry_msgs.msg import Twist


class Mover():
    def __init__(self):
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.speed = 0.5
        self.msg = Twist()

    def move(self, mess):
        rospy.loginfo("Received message: "+mess+" speed:  "+str(self.speed))
        for c in mess:
            self.switch(c)
            self.pub.publish(self.msg)
        rospy.sleep(1)

    def switch(self, c):
        if c == " ":
            pass
        elif c == "x":
            self.msg.linear.x = 0
            self.msg.linear.y = 0
            self.msg.angular.z = 0
            pass
        elif c == "w":
            self.msg.linear.x = 0.2 * self.speed
            pass
        elif c == "a":
            self.msg.angular.z = 1 * self.speed
            pass
        elif c == "s":
            self.msg.linear.x = -0.2 * self.speed
            pass
        elif c == "d":
            self.msg.angular.z =-1 * self.speed
            pass
        elif c == "+":
            rel = min(self.speed+0.2, 1)/self.speed
            self.speed = min(self.speed+0.2, 1)
            self.msg.linear.x = self.msg.linear.x*rel
            self.msg.linear.y = self.msg.linear.y*rel
            self.msg.angular.z = self.msg.angular.z*rel
            rospy.loginfo(" speed:  "+str(self.speed))
            pass
        elif c == "-":
            rel = max(self.speed-0.2, 0.01)/self.speed
            self.speed = max(self.speed-0.2, 0.01)
            self.msg.linear.x = self.msg.linear.x*rel
            self.msg.linear.y = self.msg.linear.y*rel
            self.msg.angular.z = self.msg.angular.z*rel
            rospy.loginfo(" speed:  "+str(self.speed))
            pass
        elif c == "e":
            self.msg.linear.y = -0.5 * self.speed
            pass
        elif c == "q":
            self.msg.linear.y = 0.5 * self.speed
            pass

ser = serial.Serial()
ser.baudrate = 9600
ser.port = "/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-port0"
ser.dtr = False
ser.timeout = 0.5
ser.open()

ser.flushInput()

if __name__ == '__main__':
    rospy.init_node("mover")
    m = Mover()
    while not rospy.is_shutdown():
        pack = ser.read(1024)
        mess = pack.decode().strip().lower()
        if not mess == "":
            m.move(mess)
            

    
    
    

    

   