#!/usr/bin/env python

from turtle import backward
import serial, rospy, re, sys
from std_msgs.msg import String

print(sys.getdefaultencoding())

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
        
        pub = rospy.Publisher('/rosacomms/hydromea/in', String, queue_size=10)
        filled_msg = ''
        
        print("connected to: " + ser.portstr)
        while not rospy.is_shutdown():
            if ser.in_waiting > 0:
                msg = ser.readline()
                msg_b = msg.decode(encoding = 'ascii', errors = 'strict')
                #time.sleep(0.5)
                if msg_b != '':
                    #print(msg_b)
                    if msg_b == '\n':
                        filled_msg += msg_b
                        print(filled_msg)
                        pub.publish(filled_msg)
                        filled_msg = ''
                    else:
                        filled_msg += msg_b
        rospy.spin()
        
        
if __name__ == '__main__':
    #while not rospy.is_shutdown():
    a = receiver()