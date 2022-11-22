#!/usr/bin/env python

import serial, zlib

class test:
    def __init__(self):
        self.ser1 = serial.Serial(
            port = '/dev/pts/2',\
            baudrate = 115200,\
            parity = serial.PARITY_NONE,\
            stopbits = serial.STOPBITS_ONE,\
            bytesize = serial.EIGHTBITS,\
            timeout = 0)
        
        self.ser2 = serial.Serial(
            port = '/dev/pts/3',\
            baudrate = 115200,\
            parity = serial.PARITY_NONE,\
            stopbits = serial.STOPBITS_ONE,\
            bytesize = serial.EIGHTBITS,\
            timeout = 0)

    def gen_msg(self, size):
        msg_bytes = ""
        for x in range(size):
            msg_bytes += "a"
        msg_bytes += "\n"

        self.ser1.write(msg_bytes)
        msg = self.ser2.readline()
        print(len(msg))
        
    def full_run(self):
        for x in range(1, 10000):
            self.gen_msg(x)

if __name__ == '__main__':
    a = test()
    a.full_run()