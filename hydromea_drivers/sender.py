#!/usr/bin/env python

import serial, rospy, os, pty, bz2
from std_msgs.msg import String

class sender:
    def __init__(self):
        self.ser = serial.Serial(
            #port='/dev/ttyUSB1',\
            port='/dev/pts/3',\
            baudrate=115200,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
            timeout=0)
       
        #self.master, self.slave = pty.openpty()
        #s_name = os.ttyname(self.slave)
        
        #self.ser = serial.Serial(s_name)
        
        print('Port'.ljust(25) + 'Baudrate')
        print(str(self.ser.name).ljust(25) + str(self.ser.baudrate))

        rospy.init_node('hydromea_sender')
        rospy.Subscriber('/rosacomms/hydromea/out', String, self.sender_callback)
        rospy.spin()

    def sender_callback(self, string):
        msg = string.data
        msg += '\n'
        msg = msg.encode('ascii')
        compressed_msg = bz2.compress(msg)
        self.ser.write(compressed_msg)
        print(len(msg))
        print(len(compressed_msg))
        print(float(len(msg))/float(len(compressed_msg)))
        
        #p = bz2.decompress(compressed_msg)
        #print(p)
        print('Publishing: ' +string.data+ ' as ' +compressed_msg)
        #print('Published: '+ self.ser.readline())
        
if __name__ == '__main__':
    while not rospy.is_shutdown():
        a = sender()