#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from proper_lpg.msg import Emotions
import time
from collections import Counter

emotion_dict={
    "happy":"joy",
    "surprise":"joy",
    "angry": "anger",
    "disgust": "sadness",
    "fear": "anger",
    "neutral": "neutral",
    "sad": "sadness"
}


final_map={
    "joy":{"map":"H","prob":0},
    "neutral":{"map":"N","prob":0},
    "anger":{"map":"A","prob":0},
    "sadness":{"map":"S","prob":0}
}

emotion_dict_f={}
emotion_dict_s={}
new_emotion=False
new_speech=False
window_emotion=[]
window_speech=[]
window_probs=[]

def init_map():
    global final_map
    final_map={
        "joy":{"map":"H","prob":0},
        "neutral":{"map":"N","prob":0},
        "anger":{"map":"A","prob":0},
        "sadness":{"map":"S","prob":0}
    }

def compute_probabilities(window):
    global emotion_dict_f
    emotion_dict_f=Counter(window)
    for x in emotion_dict_f:
        emotion_dict_f[x]=emotion_dict_f[x]/len(window)
  
def callback_face(data):
    global emotion_dict, new_emotion, window_emotion
    window_emotion=[]
    for w in data.w_emotions:
        window_emotion.append(emotion_dict[w]) 
    compute_probabilities(window_emotion)
    new_emotion=True

def callback_speech(data):
   global new_speech, window_speech, window_probs, emotion_dict_s
   window_speech=data.w_emotions
   window_probs=data.probs
   for i in range(len(window_speech)):
       emotion_dict_s[window_speech[i]]=window_probs[i]
   #remap the fear on the anger
   emotion_dict_s["anger"]=emotion_dict_s["anger"]+emotion_dict_s["fear"]
   new_speech=True

def publish_emotion():
    global new_emotion, new_speech, emotion_dict_s, emotion_dict_f, em_pub,final_map, threshold
    init_map()
    sum_probs=0
    if new_emotion or new_speech:
        if new_speech:
            print(emotion_dict_s)
            final_map["anger"]["prob"]=emotion_dict_s["anger"]
            final_map["sadness"]["prob"]=emotion_dict_s["sadness"]
            final_map["joy"]["prob"]=emotion_dict_s["joy"]
            for s in emotion_dict_s:
                sum_probs+=emotion_dict_s[s]
            new_speech=False
        if new_emotion:
            print(emotion_dict_f)
            final_map["anger"]["prob"]=final_map["anger"]["prob"]+emotion_dict_f["anger"]
            final_map["sadness"]["prob"]=final_map["sadness"]["prob"]+emotion_dict_f["sadness"]
            final_map["joy"]["prob"]=final_map["joy"]["prob"] + emotion_dict_f["joy"]
            final_map["neutral"]["prob"]=emotion_dict_f["neutral"]
            
            for s in emotion_dict_f:
                sum_probs+=emotion_dict_f[s]
            new_emotion=False
        max=0
        em=""
        for fm in final_map:
            final_map[fm]["prob"]=final_map[fm]["prob"]/sum_probs
            if final_map[fm]["prob"]>max:
                max=final_map[fm]["prob"]
                em=fm
        print(final_map)
        if max>=threshold:
            print(final_map[em]["map"])
            em_pub.publish(final_map[em]["map"])
        
   
        
   

if __name__ == '__main__':
    global em_pub, threshold
    rospy.init_node('emotion_estimation')
    threshold=0.5
    em_pub = rospy.Publisher('/emotion', String, queue_size=10)
    rospy.Subscriber("/face_emotion", Emotions, callback_face)
    rospy.Subscriber("/speech_emotion", Emotions, callback_speech)
    while not rospy.is_shutdown():
        time.sleep(1)
        publish_emotion()