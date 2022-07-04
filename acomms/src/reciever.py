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
        #print(unparsed_msg.data)
        #print(type(unparsed_msg.data))
        
        parsed_msg = json.loads(unparsed_msg.data)
        #print(type(msg))
        #print(msg)
        topic = parsed_msg['topic']
        msg = parsed_msg['msg']
        data_type = parsed_msg['type']
        print(topic)
        print(msg)
        print(data_type)
        
        #publisher = rp.Publisher(topic, data_type, queue_size = None)
        #publisher.publish(msg)
        
if __name__ == "__main__":
    while not rp.is_shutdown():
        print('main')
        a = reciever()
        a._init__()