#!/usr/bin/env python

import rospy as rp
from std_msgs.msg import String
from topic_tools import ShapeShifter

class parser:
    def __init__(self):
        rp.init_node(name = "accoms", anonymous = False)
        rp.Subscriber()
        
 
if __name__ == "__main__":
    while not rp.is_shutdown:
        a = parser
        rp.Rate.sleep()