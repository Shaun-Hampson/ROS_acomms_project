#!/usr/bin/env python

import serial, rospy
from std_msgs.msg import String

class receiver:
    def __init__(self):
        rospy.init_node('hydromea_receiver')
        
        ser = serial.Serial(
        port='/dev/ttyUSB1',\
        baudrate=115200,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=0)
        
        print("connected to: " + ser.portstr)
        while 1:
            msg = ser.read()
            msg = msg.decode('ascii')
            if msg != '':
                pub = rospy.Publisher('/rosacomms/hydromea/in', String, queue_size=10)
                pub.publish(msg)
        rospy.spin()
        
        
if __name__ == '__main__':
    while not rospy.is_shutdown():
        a = receiver()
        a.__init__