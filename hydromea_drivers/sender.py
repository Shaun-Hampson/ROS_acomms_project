#!/usr/bin/env python

import serial, time, timeit, rospy
from std_msgs.msg import String

class sender:
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyUSB0',\
            baudrate=115200,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
            timeout=0)
        print(self.ser.baudrate)
        print(self.ser.name)         # check which port was really used
        print('Sender should be connected to port: 0')

        self.start = timeit.timeit()
        rospy.init_node('hydromea_sender')
        rospy.Subscriber('/rosacomms/hydromea/out', String, self.sender_callback)
        rospy.spin()

    def sender_callback(self, string):
        msg = string.data
        msg += '\n'
        #print('msg: %s' %msg)
        msg = msg.encode('ascii')
        self.ser.write(msg)
        print('Publishing: %s\n\t' %string.data)
        
if __name__ == '__main__':
    while not rospy.is_shutdown():
        a = sender()
        a.__init__()