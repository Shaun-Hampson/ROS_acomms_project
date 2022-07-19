from optparse import OptionParser
from socket import socket
import rosgraph, rospy, roslib, sys


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
  
    
def _resource_name_package(name):
    if not '/' in name:
        return None
    return name[:name.find('/')]


def _full_usage():
    print("""rosacomms is a command-line tool used for parsing messages to be sent wirelessly via acoustic modems 
    
    Commands:
    \trosacomms pub\tpublish data to topic
    
    Type rosacomms <command> -h for more detailed usage, e.g. 'rosacomms pub -h'""")


def rosacomms_pub(arg):
    """Parse incomming command to publish a message to a topic"""
    args = arg[2:]
    
    parser = OptionParser()
    
    (options, args) = parser.parse_args()
    
    if len(arg) == 0:
        parser.error('specify topic name')
    if len(arg) == 1:
        parser.error('specify topic type')
    topic_name, topic_type = args[0], args[1]
    
    _check_master()
    
    pub,msg = create_pub(topic_name, topic_type)
    
    
def create_pub(topic_name, topic_type):
    """Create a rospy publisher based on the topic name and type"""
    topic_name = rosgraph.names.script_resolve_name('rosacomms', topic_name)
    try:
        msg_class = roslib.message.get_message_type(topic_type)
    except:
        raise ROSAcommsException('Invalid topic type: %s' %topic_type)
    
    if msg_class is None:
        pkg = _resource_name_package(topic_type)
        raise ROSAcommsException("invalid message type: %s.\nIf this is a valid message type, perhaps you need to type 'rosmake %s'"%(topic_type, pkg))
    rospy.init_node('rosacomms', anonymous=True, disable_rosout=True, disable_rostime=disable_rostime)
    pub = rospy.Publisher(topic_name, msg_class, latch=latch, queue_size=100)
    return pub, msg_class


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
        else:
            _full_usage()
    except ROSAcommsException as e:
        sys.stderr.write("Error: %s" %str(e))
        