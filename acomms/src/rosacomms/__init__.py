from optparse import OptionParser
from socket import socket
from std_msgs.msg import String
from rospy_message_converter import message_converter
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


def _full_usage():
    print("""rosacomms is a command-line tool used for parsing messages to be sent wirelessly via acoustic modems 
    
    Commands:
    \trosacomms pub\tpublish data to topic
    
    Type rosacomms <command> -h for more detailed usage, e.g. 'rosacomms pub -h'""")


def rosacomms_pub(arg):
    """Parse incomming command to publish a message to a topic"""
    args = arg[2:]
    
    parser = OptionParser()
    parser.add_option("-l", '--line', dest="latch", default=False, action="store_true", help="enable latching, ")
    
    (options, args) = parser.parse_args()
    
    if len(arg) == 0:
        parser.error('specify topic name')
    if len(arg) == 1:
        parser.error('specify topic type')
    topic_name, topic_type = args[0], args[1]
    
    _check_master()
    
    rospy.init_node('rosacomms', anonymous=True)
    pub = rospy.Publisher("/acomms/in", String, latch=True, queue_size=1)
    rospy.Rate(0.5)
    

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
        