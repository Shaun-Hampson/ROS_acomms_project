# ROS_acomms_project
A repo to store a ROS workspace handling the conversion of messages into a form tranmittable via acoustic waves for the communication of data to a submersable robot

## Notes
Could see about using `TopicType, topic_str, _ = rostopic.get_topic_class('/some/topic')` to accuire the topic type and message (also succeeds in part of the requirements for the interface bewteen the exsiting system and the new code), currently `type(topic_type)` retuns a long string with additional characters that is not needed and returning it back to an object maybe tricky. __Not needed in the end__

`message_class = roslib.message.get_message_class(message_type)`
`message = message_class()`

Acoustics driver needs to packet information being sent. Look up the packeting from the Hydromea. My driver might packet it anyway.

Look again at ros_serial & ros_bridge

socat -d -d pty,raw,echo=0 pty,raw,echo=0
