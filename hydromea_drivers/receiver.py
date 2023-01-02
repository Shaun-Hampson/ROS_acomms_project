#!/usr/bin/env python

import serial, rospy, sys, bz2
from std_msgs.msg import String

class receiver:
    def __init__(self):
        rospy.init_node('hydromea_receiver')
        
        ser = serial.Serial(
            #port='/dev/ttyUSB0',\
            port='/dev/pts/7',\
            baudrate=115200,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
            timeout=0)
        
        print('Port'.ljust(25) + 'Baudrate'.ljust(25) + 'decoding')
        print(str(ser.name).ljust(25) + str(ser.baudrate).ljust(25) + sys.getdefaultencoding())
        
        #os.read(master, 1000)
        
        pub = rospy.Publisher('/rosacomms/hydromea/in', String, queue_size=10)
        filled_msg = ''
        
        decompressor = bz2.BZ2Decompressor()
        
        while not rospy.is_shutdown():
            if ser.in_waiting > 0:
                msg = ser.readline()
                #print(compressed_msg)
                #msg = decompressor.decompress(compressed_msg)
                #msg = msg.decode(encoding = 'ascii', errors = 'strict')
                #time.sleep(0.5)
                if msg != '':
                    print(msg)
                    if msg == '\n':
                        filled_msg += msg
                        print(filled_msg)
                        pub.publish(filled_msg)
                        filled_msg = ''
                    else:
                        filled_msg += msg
        rospy.spin()
        
        
if __name__ == '__main__':
    #while not rospy.is_shutdown():
    a = receiver()