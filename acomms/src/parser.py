#!/usr/bin/env python

import rospy as rp
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
#from topic_tools import ShapeShifter #TODO: cannot import ShapeShifter
from rospy_message_converter import message_converter


rp.init_node(name = "acomms", anonymous = False)
publisher = rp.Publisher('/acomms', String, queue_size=10)

a = PoseStamped()
#a.header = 'acomms' #TODO: throws error here as the message converter isnt hadling this string
a.pose.position.x = 1
a.pose.position.y = 1
a.pose.position.z = 0
a.pose.orientation.w = 1

      
b = message_converter.convert_ros_message_to_dictionary(a)

msg = [
    {"topic": "/test"},
    {"type": type(a)},
    {"msg": b}
]

c = String()
c.data = msg

publisher.publish(c)