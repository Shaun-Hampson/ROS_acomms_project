#!/usr/bin/env python

import serial, rospy
from std_msgs.msg import String

class sender:
    def __init__(self):
        self.ser = serial.Serial(
            port = '/dev/ttyUSB1',\
            baudrate = 115200,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
            timeout = 0)

        print('Port'.ljust(25) + 'Baudrate')
        print(str(self.ser.name).ljust(25) + str(self.ser.baudrate))
        
        rospy.init_node('Nanomodem_sender')
        rospy.Subscriber('/rosacomms/nanomodem/out', String, self.sender_callback)
        rospy.spin()
        
        self.count = 0
        
    def sender_callback(self, string):
        self.count += 1
        msg = string.data
        msg += '\n'
        msg = msg.encode('ascii')
        self.ser.write(msg)
        print(str(self.count + '.').ljust(5) + '%s\n\t' %string.data)
        
if __name__ == '__main__':
    while not rospy.is_shutdown():
        a = sender()