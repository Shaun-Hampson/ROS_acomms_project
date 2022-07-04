# ROS_acomms_project
A repo to store a ROS workspace handling the conversion of messages into a form tranmittable via acoustic waves for the communication of data to a submersable robot

## Notes
Could see about using `TopicType, topic_str, _ = rostopic.get_topic_class('/some/topic')` to accuire the topic type and message (also succeeds in part of the requirements for the interface bewteen the exsiting system and the new code), currently `type(topic_type)` retuns a long string with additional characters that is not needed and returning it back to an object maybe tricky.