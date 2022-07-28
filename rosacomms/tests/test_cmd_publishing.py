#!/usr/bin/env python

from std_msgs.msg import *
from geometry_msgs.msg import *
import rospy

def __init__():
    rospy.init_node("test")

    """Subscribers used for testing different parts of the acomms proccess"""
    #test strings can be sent from the rosacomms command-line tool
    rospy.Subscriber("/test/String", String, general_callback())
    
    #test poses can be sent from the rosacomms command-line tool
    rospy.Subscriber("/test/Pose", Pose, general_callback()) 


def general_callback(msg):
    print('received message')
    print(msg)