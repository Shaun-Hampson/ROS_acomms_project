#!/usr/bin/env python

import rospy as rp
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from rospy_message_converter import message_converter
import json


rp.init_node(name = "acomms", anonymous = False)
publisher = rp.Publisher('/rosacomms/hydromea/in', String, queue_size=10)
rate = rp.Rate(0.5)
rate.sleep()

a = PoseStamped()
a.header.frame_id = 'acomms'
a.pose.position.x = 1
a.pose.position.y = 1
a.pose.position.z = 0
a.pose.orientation.w = 1

b = message_converter.convert_ros_message_to_dictionary(a)

msg =  {
    "topic": "/test",
    "type": str(a._type),
    "msg": b}

c = String()
c.data = json.dumps(msg)

print(c)

#d = json.loads(c.data)  #test line
#print(d)    #test line
publisher.publish(c)