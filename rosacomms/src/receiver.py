#!/usr/bin/env python

from pickle import TRUE
import rospy as rp
import roslib
from std_msgs.msg import String
from geometry_msgs.msg import *
from rospy_message_converter import message_converter
import json

class ReceiverException(Exception):
    pass

class reciever:
    def __init__(self):
        rp.init_node('receiver')
        modem = rp.get_param('modem_type')
        print('setup')
        rp.Subscriber('/rosacomms/'+modem+'/in', String, self.extract)
        rp.spin()
        
    def extract(self, unparsed_msg):
        print("received message")
        #print(unparsed_msg.data)
        #print(type(unparsed_msg.data))
        try:
            parsed_msg = json.loads(unparsed_msg.data)
            topic = parsed_msg['topic']
            #msg = str(parsed_msg['msg']).replace("\'", "\"")
            msg = parsed_msg['msg']
            data_type = parsed_msg['type']
            print(topic)
            #print(msg)
            print(data_type)
        except:
            raise ReceiverException("failed to load JSON message")
        #print(type(msg))
        #print(type(roslib.message.get_message_class(data_type)))
        
        msg = message_converter.convert_dictionary_to_ros_message(data_type, msg)
        publisher = rp.Publisher(topic, roslib.message.get_message_class(data_type), queue_size = 1, latch=TRUE)
        print(msg)
        print('\n')
        publisher.publish(msg)
        
if __name__ == "__main__":
    while not rp.is_shutdown():
        print('main')
        a = reciever()
        a.__init__()