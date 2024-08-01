#!/usr/bin/env python
# -*- coding: utf-8 -*-

from get_parameters import *
from personality_generator import *
import requests
from emotion_generation import *
from chat_playground import *

url='http://127.0.0.1:5019/'

headers= {'Content-Type':'application/json'}

data_action={
        "robot_emotion":"",
        "sentence":"",
        "volume":"",
        "gaze":"",
        "tone":"",
        "gesture_amplitude":"",
        "head":""
         
}

def dispatch_action(action, personality, user_emotion, user_sentence, comfortability):
        
        params=generate_params(personality, action)
        mmap =get_map(params,personality)
        action=action.replace("_"," ").lower()
        print("otput personality generator********************")
        print(mmap,action,personality)
        if ("react" not in action) and ("compute" not in action) and ("check" not in action):
                print("generate the current robot emotion ********************")
                robot_emotion= generate_emotion( user_sentence, user_emotion, comfortability, personality)
                #robot_emotion="Angry"
                print(robot_emotion)
                robot_sentence, tone = generate_sentence(user_emotion, robot_emotion, user_sentence, personality, mmap["language"], action)
                print(robot_sentence)
                data_action["robot_emotion"]=robot_emotion
                data_action["sentence"]=robot_sentence
                data_action["volume"]=mmap["volume"]
                data_action["gaze"]=mmap["gaze"]
                data_action["tone"]=tone
                data_action["gesture_amplitude"]=mmap["amplitude"]
                data_action["head"]=mmap["head"]
                print(data_action)
                resp=requests.put(url+'exec_action', json=data_action, headers=headers)
        return True, action
        
    





        
