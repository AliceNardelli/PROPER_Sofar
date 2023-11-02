#!/usr/bin/env python
import rospy
from std_msgs.msg import String

emotion_dict={
    "happy":"H",
    "surprise":"H",
    "angry": "A",
    "disgust": "S",
    "fear": "A",
    "neutral": "N",
    "sad": "S"
}

emotion=""
new_emotion=False
new_touch=False

def callback_emotion(data):
   global emotion, emotion_dict, new_emotion
   emotion=emotion_dict[data.data]
   new_emotion=True

def callback_touch(data):
   global new_touch
   new_touch=True

def publish_perception():
    global emotion,  new_emotion, new_touch
    if new_touch:
        t="T_"
    else:
        t="NT_"
        new_touch=False
    if new_emotion:
        tot=t+emotion
        perc_pub.publish(tot)
        new_emotion=False
    else:
        tot=t+"N"
        
   

if __name__ == '__main__':
    global perc_pub
    rospy.init_node('perception_interface')
    perc_pub = rospy.Publisher('/perception', String, queue_size=10)
    rospy.Subscriber("/emotion", String, callback_emotion)
    rospy.Subscriber("/touch", String, callback_touch)
    while not rospy.is_shutdown():
        publish_perception()