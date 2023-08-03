# ROS_acomms_project
A ROS package for handling wireless communication of ROS topic publish commands via arbitrary communication mediums.

ROSAcomms provides a commandline tool that takes a topic name and type and a message and parses it to a standard form suitable for wireless transmission. As ROSAcomms is intended to be for sending messages between two unconnected ROS systems, another parser is provided for the receiving ROS system to tur the standard form message back into a form used by ROS. For sending and receiving the standard form message, modem driver programmes are required.

![](/assets/Systemdiagram.drawio.png?raw=true "ROSAcomms System Diagram")


## Direction for use
### Required Packages
Please ensure you have the [***rospy_message_converter***](https://github.com/uos/rospy_message_converter) installed.

### Usage
The correct drivers need to be running before a message can be sent. Two drivers are already provided:\
Hydromea LUMA 250LP -> optical communication\
Nanomodem v3 -> acoustic communication\
These drivers may be used for other modems of the same communication medium, however if custom drivers are needed please see the __Adding Custom Drivers__ section for how to do this.

The receiver parser uses a default modem provided to its launch file via the config file. When changing the modem being used the modem in the config file needs to be set to the correct one. The receiver parser can be launched using:\
`$ roslaunch rosacomms receiver.launch`

Once the drivers and the receiver parser are running, messages can be sent between the two ROS systems. Using the commandline tool the system can be provided with the information for the desired topic to be published to and the rosmessage containing the required data.\
To publish using the default modem:\
`$ rosacomms pub topic_name topic_type message`\
To publish using a non-default modem use the device (-d) option:\
`$ rosacomms pub topic_name topic_type message -d modem_name`

### Adding Custom Drivers
To add custom divers to ROSAcomms, the config file needs to be updated with the name of the modem. In the `if/else` block in `rosacomms_pub()` in _/src/rosacomms/\_\_init\_\_.py_ a new device option for the new modem's name needs to be added othrwise the modem will not be recognised. This option allows the commandline tool to publish to the correct topic that the new sender driver uses.


## User Notice
ROSAcomms is intended to be open-source. Please use as required. Feedback and questions are welcomed.


## Development Notes
### code notes
`message_class = roslib.message.get_message_class(message_type)`\
`TopicType, topic_str, _ = rostopic.get_topic_class('/some/topic')`\
socat -d -d pty,raw,echo=0 pty,raw,echo=0

### Areas for work
#### Light tasks
1. Launching of modem drivers is a hassle, system needs to launch the desired modem driver upon launch.
2. Commenting of code should be given as future edits may require the need to re-understand the code.

#### Heavy tasks
1. Acoustic modem drivers needs the catch for messages being send to be updated. Look at using two bytes in each message for representing the number of message parts and the number for each part received.
2. Add in ROS serivce calling into the project.
3. A more suitable user interface should be implemented if possible. This my conflict with the current build of ROSAcomms.