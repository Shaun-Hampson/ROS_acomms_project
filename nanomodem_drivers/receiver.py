#!/usr/bin/env python

import serial, rospy, zlib
from std_msgs.msg import String

class receiver:
    def __init__(self):
        rospy.init_node('nanomodem_receiver')
        
        ser = serial.Serial('/dev/ttyUSB1', 9600, 8, serial.PARITY_NONE, serial.STOPBITS_ONE, 0.1)
        
        print('Port'.ljust(25) + 'Baudrate'.ljust(25) + 'ID'.ljust(25) + 'Voltage'.ljust(25))
        cmd_string = '$?'
        cmd_bytes = cmd_string.encode('utf-8')
        ser.write(cmd_bytes)
        starting_msg = ser.readline()
        address = starting_msg[2:5]
        voltage = float(starting_msg[6:11])*0.0002288818359375
        print(str(ser.name).ljust(25) + str(ser.baudrate).ljust(25) + str(address).ljust(25) + str(voltage).ljust(25))
        
        pub = rospy.Publisher('/rosacomms/nanomodem/in', String, queue_size=10)
        
        
        while not rospy.is_shutdown():
            if ser.in_waiting > 0:
                stop = False
                filled_msg = ''
                a = []
                while stop == False:
                    msg = ser.readline()
                    if msg != '':
                        print(msg)
                        a.append(msg)
                    #print(a[i])
                    #print('while')
                    #print(a[i][5:7])
                    #if a[i][5:7] != '64':
                    #if a[i][-1:] == '#':
                        #print('if')
                        #for b in a:
                            #filled_msg = filled_msg.join(b[7:])
                        #print(filled_msg)
                        if msg[-3] == '#':
                            stop = True
                print(a)
                for b in a:
                    if b[0:2] == '#B' and b[-2:] == '\r\n':
                        filled_msg = filled_msg +b[7:-2]
                    elif b[0:2] == '#B':
                        filled_msg = filled_msg + b[7:]
                    elif b[-2:] == '\r\n':
                        filled_msg = filled_msg + b[0:-2]
                    else:
                        filled_msg = filled_msg + b
                filled_msg = filled_msg[0:(len(filled_msg)-1)]
                print(filled_msg)
                try:
                    msg_to_pub = zlib.decompress(filled_msg)
                    print(msg_to_pub)
                except:
                    msg_to_pub = filled_msg
                pub.publish(msg_to_pub)
                print('\n')
                #msg = ser.readline()
                #print('Here' + msg)
                #if msg[-1] == '\n':
                #    filled_msg += msg
                #    try:
                #        decompressed_msg = zlib.decompress(filled_msg)
                #        msg = decompressed_msg
                #        print('decomp')
                #    except:
                #        msg = filled_msg
                #        print('no decomp')
                #    pub.publish(msg)
                #    filled_msg = ''
                #else:
                #    filled_msg += msg
        rospy.spin()
        

if __name__ == '__main__':
    a = receiver()