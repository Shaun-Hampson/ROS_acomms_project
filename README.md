# ROS_acomms_project
A ROS package for handling wireless communication of ROS topic publish commands via arbitrary communication mediums.


## Direction for use
### Required Packages
Please ensure you have the [***rospy_message_converter***](https://github.com/uos/rospy_message_converter)

### Usage



## Notes
Could see about using `TopicType, topic_str, _ = rostopic.get_topic_class('/some/topic')` to accuire the topic type and message (also succeeds in part of the requirements for the interface bewteen the exsiting system and the new code), currently `type(topic_type)` retuns a long string with additional characters that is not needed and returning it back to an object maybe tricky. __Not needed in the end__

`message_class = roslib.message.get_message_class(message_type)`
`message = message_class()`

Acoustics driver needs to packet information being sent. Look up the packeting from the Hydromea. My driver might packet it anyway.

Look again at ros_serial & ros_bridge

socat -d -d pty,raw,echo=0 pty,raw,echo=0

discuss try/catch in decompressing incoming msgs