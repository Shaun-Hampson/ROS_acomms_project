#!/usr/bin/env python

import rospy as rp
from std_msgs.msg import String
import geometry_msgs.msg
from rospy_message_converter import json_message_converter
import json

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
        print(globals()[data_type])
        
        publisher = rp.Publisher(topic, a, queue_size = None)    
        #TODO: need to find a way of turning a string back to the 
        # desired object type for the message
        publisher.publish(msg)
        
if __name__ == "__main__":
    while not rp.is_shutdown():
        print('main')
        a = reciever()
        a._init__()