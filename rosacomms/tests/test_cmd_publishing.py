#!/usr/bin/env python

from std_msgs.msg import *
from geometry_msgs.msg import *
import rospy


class test:
    
    def __init__(self):
        rospy.init_node("test")
        """Subscribers used for testing different parts of the acomms proccess"""
        #test strings can be sent from the rosacomms command-line tool
        #rospy.Subscriber("/test/String", String, self.general_callback)
        
        #test rosacomms/out
        rospy.Subscriber("/rosacomms/out", Pose, self.general_callback)
        
        rospy.spin()


    def general_callback(self, msg):
        print('received message')
        print(msg)
    
    
if __name__ == "__main__":
    while not rospy.is_shutdown():
        print('main')
        a = test()
        a.__init__()
