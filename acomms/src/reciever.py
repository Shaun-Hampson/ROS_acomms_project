#!/usr/bin/env python

import rospy as rp
from std_msgs.msg import String
import json

class reciever:
    def _init__(self):
        rp.init_node('reciever')
        print('setup')
        rp.Subscriber('/acomms', String, self.extract)
        rp.spin()
        
    def extract(self, unparsed_msg):
        print("msg recieved")
        #data_type = json.loads(unparsed_msg['type'])
        #destination_topic = json.loads(unparsed_msg['topic'])
        #msg = json.loads(unparsed_msg['msg'])
        #publisher = rp.Publisher(destination_topic, data_type, queue_size = None)
        
if __name__ == "__main__":
    while not rp.is_shutdown():
        print('main')
        a = reciever()
        a._init__()