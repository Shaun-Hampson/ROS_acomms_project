#!/usr/bin/env python

import rospy as rp
from std_msgs.msg import String
import json

class reciever:
    def _init__(self):
        rp.Subscriber("/acomms/out", String, self.extract)
        
    def extract(self, unparsed_msg):
        parsed_msg = json.loads(unparsed_msg)
        data_type = parsed_msg['data_type']
        destination_topic = parsed_msg['topic']
        msg = parsed_msg['msg']
        publisher = rp.Publisher(destination_topic, data_type, queue_size = None)