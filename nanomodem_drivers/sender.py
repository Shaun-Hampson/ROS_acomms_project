#!/usr/bin/env python

from encodings import utf_8
import serial, rospy, zlib, time, math
from std_msgs.msg import String

class sender:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, 8, serial.PARITY_NONE, serial.STOPBITS_ONE, 0.1)

        cmd_string = '$?'
        cmd_bytes = cmd_string.encode('utf-8')
        self.ser.write(cmd_bytes)
        msg = self.ser.readline()
        node_ID = msg[2:5]
        voltage = float(msg[6:11])*0.0002288818359375
        
        print('Port'.ljust(25) + 'Baudrate'.ljust(25) + 'ID'.ljust(25) + 'Voltage'.ljust(25))
        print(str(self.ser.name).ljust(25) + str(self.ser.baudrate).ljust(25) + node_ID.ljust(25) + str(voltage).ljust(25) + '\n')
        
        rospy.init_node('Nanomodem_sender')
        rospy.Subscriber('/rosacomms/nanomodem/out', String, self.sender_callback)
        rospy.spin()
        
    def sender_callback(self, string):
        msg = string.data
        compressed_msg = zlib.compress(msg)
        ratio = float(len(msg))/float(len(compressed_msg))
        if ratio > 1:
            self.write_msg(compressed_msg)
            print('Compressing msg\n')
        else:
            self.write_msg(msg)
            print('Msg does not need compressed\n')
        #print(self.ser.readline())       
        #print('%s\n\t' %string.data)
        
    def write_msg(self, msg):
        #print('here')
        msg += '#'
        print('No. of parts to send: ' + str(int(math.ceil(len(msg)/float(64)))))
        run_once_more = False
        while len(msg) > 64 or run_once_more == True:
            time.sleep(3)
            msg_prt = msg[0:64]
            cmd_string = '$B' + '{:02d}'.format(len(msg_prt)) + msg_prt
            #cmd_bytes = cmd_string.encode('utf-8')
            #print(cmd_bytes)
            if self.ser.write(cmd_string) != len(cmd_string):
                print('Error')
            size = (len(msg)-64)
            msg = msg[-size:]
            #print(len(msg))
            if len(msg) > 0 and size > 0:
                run_once_more = True
            else:
                run_once_more = False
        
if __name__ == '__main__':
    while not rospy.is_shutdown():
        a = sender()