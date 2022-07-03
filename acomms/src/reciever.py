#!/usr/bin/env python

from simplejson import loads
import rospy as rp
from std_msgs.msg import String
from rospy_message_converter import json_message_converter
import json
import ast

class reciever:
    def _init__(self):
        rp.init_node('reciever')
        print('setup')
        rp.Subscriber('/acomms', String, self.extract)
        rp.spin()
        
    def extract(self, unparsed_msg):
        print("msg recieved")
        
        #publisher = rp.Publisher(destination_topic, data_type, queue_size = None)
        #publisher.publish(msg)
        
if __name__ == "__main__":
    while not rp.is_shutdown():
        print('main')
        a = reciever()
        a._init__()