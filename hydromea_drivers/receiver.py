#!/usr/bin/env python

import serial, rospy, time
from std_msgs.msg import String

class receiver:
    def __init__(self):
        rospy.init_node('hydromea_receiver')
        
        ser = serial.Serial(
        port='/dev/ttyUSB0',\
        baudrate=115200,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=0)
        
        pub = rospy.Publisher('/rosacomms/hydromea/in', String, queue_size=10)
        filled_msg = ''
        
        print("connected to: " + ser.portstr)
        while not rospy.is_shutdown():
            msg = ser.read()
            msg = msg.decode('ascii')
            #time.sleep(0.5)
            if msg != '':
                filled_msg += msg
                pub.publish(filled_msg)
        rospy.spin()
        
        
if __name__ == '__main__':
    while not rospy.is_shutdown():
        a = receiver()
        a.__init__