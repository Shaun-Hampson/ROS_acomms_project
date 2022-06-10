#!/usr/bin/env python

import rospy as rp
from std_msgs.msg import String

class accoms:
    def __init__(self):
        rp.init_node(name = "accoms", anonymous = False)
        msg_pub = rp.Publisher("parser", String, queue_size=10)
        accoms_msg = String()
        
        accoms_msg.data = "testing"
        msg_pub.publish(accoms_msg)

if __name__ == "__main__":
    while not rp.is_shutdown:
        a = accoms
        rp.Rate.sleep(100)
        
#TODO: set up a subsriber to publish test data to, work out why this thing wont stop shutting down