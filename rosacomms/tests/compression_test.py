#!/usr/bin/env python

import bz2, zlib, pylzma
import string, random
import csv, json
from std_msgs.msg import String
from geometry_msgs.msg import Pose, PoseStamped, PoseWithCovarianceStamped
from rospy_message_converter import message_converter
import rospy

def generate_string(size):
    letters = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    return ''.join(random.choice(letters) for i in range(size))

def generate_rosmsg(option, size):
    letters = string.ascii_letters
    numbers = string.digits
    now = rospy.Time.now()
    print(now)
    
    if option == 1:
        topic_type = String()
        msg = String()
        msg.data = generate_string(size)
    
    elif option == 2:
        topic_type = Pose()
        msg = Pose()
        msg.position.x = ''.join(random.choice(numbers) for i in range(size))
        msg.position.y = ''.join(random.choice(numbers) for i in range(size))
        msg.position.z = ''.join(random.choice(numbers) for i in range(size))
        msg.orientation.x = ''.join(random.choice(numbers) for i in range(size))
        msg.orientation.y = ''.join(random.choice(numbers) for i in range(size))
        msg.orientation.z = ''.join(random.choice(numbers) for i in range(size))
        msg.orientation.w = 1.0
    
    elif option == 3:
        topic_type = PoseStamped()
        msg = PoseStamped()
        msg.header.stamp.secs = now.secs
        msg.header.stamp.nsecs = now.nsecs
        msg.header.frame_id = ''.join(random.choice(letters) for i in range(size))
        [msg.pose.position.x, msg.pose.position.y, msg.pose.position.z] = [''.join(random.choice(numbers) for i in range(size)),
                            ''.join(random.choice(numbers) for i in range(size)),
                            ''.join(random.choice(numbers) for i in range(size))]
        [msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w] = [''.join(random.choice(numbers) for i in range(size)),
                                ''.join(random.choice(numbers) for i in range(size)),
                                ''.join(random.choice(numbers) for i in range(size)),
                                1.0]
        
    elif option == 4:
        topic_type = PoseWithCovarianceStamped()
        msg = PoseWithCovarianceStamped()
        msg.header.stamp.secs = now.secs
        msg.header.stamp.nsecs = now.nsecs
        msg.header.frame_id = ''.join(random.choice(numbers) for i in range(size))
        [msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z] = [''.join(random.choice(numbers) for i in range(size)),
                                ''.join(random.choice(numbers) for i in range(size)),
                                ''.join(random.choice(numbers) for i in range(size))]
        [msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w] = [''.join(random.choice(numbers) for i in range(size)),
                                    ''.join(random.choice(numbers) for i in range(size)),
                                    ''.join(random.choice(numbers) for i in range(size)),
                                    1.0]
        msg.pose.covariance = [''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)),
                               ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)),
                               ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)),
                               ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)),
                               ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)),
                               ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)), ''.join(random.choice(numbers) for i in range(size)),]
    return(msg, topic_type)

    
def rand_test():
    with open('compression_tests.csv', mode = 'w') as file:
        writer = csv.writer(file, delimiter=',')
        fieldnames = ['msg len',"",
                      'min len bz2', 'max len bz2', 'ave len bz2', 'min ratio bz2', 'max ratio bz2', 'ave ratio bz2', "",
                      'min len zlib', 'max len zlib', 'ave len zlib', 'min ratio zlib', 'max ratio zlib', 'ave ratio zlib', "",
                      'min len lzma', 'max len lzma', 'ave len lzma', 'min ratio lzma', 'max ratio lzma', 'ave ratio lzma']
        writer.writerow(fieldnames)
        
        for i in range(1000):
            print('here1'+str(i))
            bz2_total, zlib_total, lzma_total = 0, 0, 0
            bz2_min, zlib_min, lzma_min = 999999, 999999, 999999
            bz2_max, zlib_max, lzma_max = 0, 0, 0
            bz2_ratio_total, zlib_ratio_total, lzma_ratio_total = 0, 0, 0
            bz2_ratio_min, zlib_ratio_min, lzma_ratio_min = 999999, 999999, 999999
            bz2_ratio_max, zlib_ratio_max, lzma_ratio_max = 0, 0, 0
            for x in range(10):
                print('here2'+str(x))
                test_str = generate_string(i+1)
                bz2_str = bz2.compress(test_str)
                zlib_str = zlib.compress(test_str)
                lzma_str = pylzma.compress(test_str)
                
                #lengths of the compressed strings
                bz2_length = len(bz2_str)
                zlib_length = len(zlib_str)
                lzma_length = len(lzma_str)
                
                #compression ratios
                bz2_ratio = float(i)/float(bz2_length)
                zlib_ratio = float(i)/float(zlib_length)
                lzma_ratio = float(i)/float(lzma_length)
                
                #total length, used for calc ave length 
                bz2_total += bz2_length
                zlib_total += zlib_length
                lzma_total += lzma_length
                
                #total ratio, used for calc ave ratio
                bz2_ratio_total += bz2_ratio
                zlib_ratio_total += zlib_ratio
                lzma_ratio_total += lzma_ratio
                
                #update and store min/max lengths for each compression
                if bz2_length < bz2_min:
                    bz2_min = bz2_length
                if bz2_length > bz2_max:
                    bz2_max = bz2_length
                    
                if zlib_length < zlib_min:
                    zlib_min = zlib_length
                if zlib_length > zlib_max:
                    zlib_max = zlib_length
                    
                if lzma_length < lzma_min:
                    lzma_min = lzma_length
                if lzma_length > lzma_max:
                    lzma_max = lzma_length
                    
                #update and store min/max comprassion ratios
                if bz2_ratio < bz2_ratio_min:
                    bz2_ratio_min = bz2_ratio
                if bz2_ratio > bz2_ratio_max:
                    bz2_ratio_max = bz2_ratio
                    
                if zlib_ratio < zlib_ratio_min:
                    zlib_ratio_min = zlib_ratio
                if zlib_ratio > zlib_ratio_max:
                    zlib_ratio_max = zlib_ratio
                    
                if lzma_ratio < lzma_ratio_min:
                    lzma_ratio_min = lzma_ratio
                if lzma_ratio > lzma_ratio_max:
                    lzma_ratio_max = lzma_ratio
                    
            #ave lengths
            bz2_ave = float(bz2_total)/10
            zlib_ave = float(zlib_total)/10
            lzma_ave = float(lzma_total)/10
            
            #ave ratios
            bz2_ratio_ave = float(bz2_ratio_total)/10
            zlib_ratio_ave = float(zlib_ratio_total)/10
            lzma_ratio_ave = float(lzma_ratio_total)/10
            
            writer.writerow([i+1, "",
                             bz2_min, bz2_max, bz2_ave, bz2_ratio_min, bz2_ratio_max, bz2_ratio_ave, "",
                             zlib_min, zlib_max, zlib_ave, zlib_ratio_min, zlib_ratio_max, zlib_ratio_ave, "",
                             lzma_min, lzma_max, lzma_ave, lzma_ratio_min, lzma_ratio_max, lzma_ratio_ave])
            

def msg_test(option, size):
    with open('msg_compression_test'+str(option)+str(size)+'.csv', mode = 'w') as file:
        writer = csv.writer(file, delimiter=',')
        fieldnames = ['msg len',"",
                      'min len bz2', 'max len bz2', 'ave len bz2', 'min ratio bz2', 'max ratio bz2', 'ave ratio bz2', "",
                      'min len zlib', 'max len zlib', 'ave len zlib', 'min ratio zlib', 'max ratio zlib', 'ave ratio zlib', "",
                      'min len lzma', 'max len lzma', 'ave len lzma', 'min ratio lzma', 'max ratio lzma', 'ave ratio lzma']
        writer.writerow(fieldnames)
        
        topic_name = "/bluerov/auip/pid/request"
        msg, topic_type = generate_rosmsg(option, size)
        
        print(msg)
        
        msg_dict = message_converter.convert_ros_message_to_dictionary(msg)
        
        parsed_msg = {
            "topic": topic_name,
            "type": str(msg._type),
            "msg": msg_dict
        }
        
        c = String()
        c.data = json.dumps(parsed_msg)
        
        c = str(c)
        
        bz2_total, zlib_total, lzma_total = 0, 0, 0
        bz2_min, zlib_min, lzma_min = 999999, 999999, 999999
        bz2_max, zlib_max, lzma_max = 0, 0, 0
        bz2_ratio_total, zlib_ratio_total, lzma_ratio_total = 0, 0, 0
        bz2_ratio_min, zlib_ratio_min, lzma_ratio_min = 999999, 999999, 999999
        bz2_ratio_max, zlib_ratio_max, lzma_ratio_max = 0, 0, 0
        for x in range(10):
            bz2_str = bz2.compress(c)
            zlib_str = zlib.compress(c)
            lzma_str = pylzma.compress(c)
            
            #lengths of the compressed strings
            bz2_length = len(bz2_str)
            zlib_length = len(zlib_str)
            lzma_length = len(lzma_str)
            
            #compression ratios
            bz2_ratio = float(len(c))/float(bz2_length)
            zlib_ratio = float(len(c))/float(zlib_length)
            lzma_ratio = float(len(c))/float(lzma_length)
            
            #total length, used for calc ave length 
            bz2_total += bz2_length
            zlib_total += zlib_length
            lzma_total += lzma_length
            
            #total ratio, used for calc ave ratio
            bz2_ratio_total += bz2_ratio
            zlib_ratio_total += zlib_ratio
            lzma_ratio_total += lzma_ratio
            
            #update and store min/max lengths for each compression
            if bz2_length < bz2_min:
                bz2_min = bz2_length
            if bz2_length > bz2_max:
                bz2_max = bz2_length
                
            if zlib_length < zlib_min:
                zlib_min = zlib_length
            if zlib_length > zlib_max:
                zlib_max = zlib_length
                
            if lzma_length < lzma_min:
                lzma_min = lzma_length
            if lzma_length > lzma_max:
                lzma_max = lzma_length
                
            #update and store min/max comprassion ratios
            if bz2_ratio < bz2_ratio_min:
                bz2_ratio_min = bz2_ratio
            if bz2_ratio > bz2_ratio_max:
                bz2_ratio_max = bz2_ratio
                
            if zlib_ratio < zlib_ratio_min:
                zlib_ratio_min = zlib_ratio
            if zlib_ratio > zlib_ratio_max:
                zlib_ratio_max = zlib_ratio
                
            if lzma_ratio < lzma_ratio_min:
                lzma_ratio_min = lzma_ratio
            if lzma_ratio > lzma_ratio_max:
                lzma_ratio_max = lzma_ratio
                
        #ave lengths
        bz2_ave = float(bz2_total)/10
        zlib_ave = float(zlib_total)/10
        lzma_ave = float(lzma_total)/10
        
        #ave ratios
        bz2_ratio_ave = float(bz2_ratio_total)/10
        zlib_ratio_ave = float(zlib_ratio_total)/10
        lzma_ratio_ave = float(lzma_ratio_total)/10
        
        writer.writerow([len(c), "",
                        bz2_min, bz2_max, bz2_ave, bz2_ratio_min, bz2_ratio_max, bz2_ratio_ave, "",
                        zlib_min, zlib_max, zlib_ave, zlib_ratio_min, zlib_ratio_max, zlib_ratio_ave, "",
                        lzma_min, lzma_max, lzma_ave, lzma_ratio_min, lzma_ratio_max, lzma_ratio_ave])


if __name__ == '__main__':
    rospy.init_node('test')
    
    msg_test(1, 5)
    msg_test(1, 10)
    print('test 1 done')
    
    msg_test(2, 5)
    msg_test(2, 10)
    print('test 2 done')
    
    msg_test(3, 5)
    msg_test(3, 10)
    print('test 3 done')
    
    msg_test(4, 5)
    msg_test(4, 10)
    print('Finished')