from optparse import OptionParser
from socket import socket

from std_msgs.msg import String
from rospy_message_converter import message_converter
import rosgraph, rospy, roslib, sys, yaml, json, genpy

NAME = 'rosacomms'

class ROSAcommsException(Exception):
    pass


class ROSAcommsIOException(ROSAcommsException):
    pass


def _check_master():
        """Check connection to master"""
        try:
            rosgraph.Master('/rosacomms').getPid()
        except socket.error:
            raise ROSAcommsIOException('Unable to communicate with master')
        
def _startup(rosacomms_out):
    rospy.init_node('rosacomms', anonymous=True,  disable_rosout=True, disable_rostime=True)
    pub = rospy.Publisher(rosacomms_out, String, queue_size=10)
    rate = rospy.Rate(0.5)
    rate.sleep()
    return pub


def _full_usage():
    print("""rosacomms is a command-line tool used for parsing messages to be sent wirelessly via acoustic modems 
    
    Commands:
    \trosacomms pub\tpublish data to topic""")


def rosacomms_pub(arg):
    """Parse incomming command to publish a message to a topic"""
    args = arg[2:]
    
    parser = OptionParser(usage="usage: %prog pub /topic type [args...]", prog=NAME)
    #parser.add_option("-f", '--file', dest="file", default=False, action="store_true", help="enable latching, ")
    parser.add_option("-d", '--device', help='switches modem from hydromea to chosen device', default='hydromea')
    
    (options, args) = parser.parse_args(args)
    
    if options.device == 'hydromea':
        rosacomms_out = '/rosacomms/hydromea/out'
    elif options.device == 'evologics':
        rosacomms_out = '/rosacomms/evologics/out'
    elif options.device == 'nanomodem':
        rosacomms_out = '/rosacomms/nanomodem/out'
    if len(args) == 0:
        parser.error('specify topic name')
    if len(args) == 1:
        parser.error('specify topic type')
    topic_name, topic_type = args[0], args[1]
    
    #TODO: what is the next 6 lines doing for the programme?
    try:
        pub_args = []
        for arg in args[2:]:
            pub_args.append(yaml.safe_load(arg))
    except Exception as e:
        parser.error("Argument error: "+str(e))
    
    _check_master()
    
    pub = _startup(rosacomms_out)
    
    msg_class = roslib.message.get_message_class(topic_type)
    #print('topic name: ' + topic_name + '\n')
    #print('topic type: ' + topic_type + '\n')
    
    _publish(pub, topic_name, msg_class, pub_args)
    
    
def _publish(pub, topic_name, msg_class, pub_args):
    msg = msg_class()
    
    _fill_message(msg, pub_args)
    
    msg_dict = message_converter.convert_ros_message_to_dictionary(msg)
    
    parsed_message = {
        "topic": topic_name,
        "type": str(msg._type),
        "msg": msg_dict
    }
    
    c = String()
    c.data = json.dumps(parsed_message)
    
    print(c.data)
    
    pub.publish(c)
    
    
def rosacomms_srv(arg):
    args = arg[2:]
    
    parser = OptionParser(usage="usage: %prog srv /topic service_args [args...]", prog=NAME)
    parser.add_option("-d", "--device", help='switches modem from hydromea to chosen device', default='hydromea')
    
    (options, args) = parser.parse_args(args)
    
    with open('/home/shaun_hampson/acomms_ws/src/ROS_acomms_project/rosacomms/config/modem_setup.yaml', 'r') as file:
        file = yaml.safe_load(file)

    for i in file:
        if options.device == i:
            rosacomms_out = 'rosacomms_srv/'+ i +'/out'
            break
    if len(args) == 0:
        print('Specify service name')
    service = args[0]
    service_args = args[1:]
        
    _check_master()
    
    pub = _startup(rosacomms_out)
    
    _srv_publish(pub, service, service_args)
    
    
def _srv_publish(pub, service, service_args):
    parsed_srv_call = {
        "srv": service,
        "args": service_args
    }
    
    c = String()
    c.data = json.dumps(parsed_srv_call)
    
    pub.publish(c)
        

def _fill_message(msg, pub_args):
    try:
        # Populate the message and enable substitution keys for 'now'
        # and 'auto'. There is a corner case here: this logic doesn't
        # work if you're publishing a Header only and wish to use
        # 'auto' with it. This isn't a troubling case, but if we start
        # allowing more keys in the future, it could become an actual
        # use case. It greatly complicates logic because we'll have to
        # do more reasoning over types. to avoid ambiguous cases
        # (e.g. a std_msgs/String type, which only has a single string
        # field).

        # allow the use of the 'now' string with timestamps and 'auto' with header
        now = rospy.get_rostime()
        import std_msgs.msg
        keys = { 'now': now, 'auto': std_msgs.msg.Header(stamp=now) }
        genpy.message.fill_message_args(msg, pub_args, keys=keys)
    except genpy.MessageException as e:
        raise ROSAcommsException(str(e)+"\n\nArgs are: [%s]"%genpy.message.get_printable_message_args(msg))
    

def main(args = None):
    if args is None:
        args = sys.argv
    args = rospy.myargv(args)
    
    if len(args) == 1:
        _full_usage()
    
    try:
        command = args[1]
        if command == 'pub':
            rosacomms_pub(args)
        if command == 'srv':
            rosacomms_srv(args)
        else:
            _full_usage()
    except ROSAcommsException as e:
        sys.stderr.write("Error: %s" %str(e))
        