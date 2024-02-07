#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import time
import requests
url='http://127.0.0.1:8001/'
headers= {'Content-Type':'application/json'}

data = {
}

def publish_perception():
    global perc_pub
    resp=requests.put(url+'get_input', json=data, headers=headers)
    new_perception=eval(resp.text)["new_perception"]  
    if new_perception=="True":
        perc=eval(resp.text)["perception"]
        msg=String()
        msg.data=perc

        perc_pub.publish(msg)

        
   

if __name__ == '__main__':
    global perc_pub
    rospy.init_node('perception_interface')
    perc_pub = rospy.Publisher('/perception', String, queue_size=10)
    while not rospy.is_shutdown():
        time.sleep(1)
        publish_perception()