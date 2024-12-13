#!/usr/bin/env python
# -*- coding: utf-8 -*-

from get_parameters import *
from personality_generator import *
import requests
from emotion_generation import *
from chat_playground import *

url='http://127.0.0.1:5021/'

headers= {'Content-Type':'application/json'}

data_action={
        "emotion":"",
        "volume":"",
        "gaze":"",
        "language_style":"",
        "action":"",
        "personality":""       
}

traits_res=["Extrovert","Introvert","Conscientious","Unscrupolous","Agreeable","Disagreeable"]

file_name="/home/alice/Rose/prova.txt"
file = open(file_name, 'a')

def dispatch_action(action, personality, personality_emotions, user_emotion, user_sentence, comfortability, weights_res):
        
        params=generate_params(personality, action)
        mmap =get_map(params,personality)
        personality_sentence=""
        language_sentence=""
        for i in range(len(weights_res)):
                if weights_res[i]!=0:
                        personality_sentence=personality_sentence+" "+traits_res[i]
                        if traits_res[i]==personality:
                                language_sentence=language_sentence+" "+mmap["language"]
                        else:
                                params_l=generate_params(traits_res[i], action)
                                mmap_l =get_map(params_l,traits_res[i])
                                language_sentence=language_sentence+" "+mmap_l["language"]
        print("PERSONALITY and LANGUAGE paramos: "+ personality_sentence+" "+language_sentence)
        action=action.replace("_"," ").lower()
        print("otput personality generator********************")
        print(mmap,action,personality)
        if ("react" not in action) and ("compute" not in action) and ("check" not in action):
                print("generate the current robot emotion ********************")
                robot_emotion= generate_emotion( user_sentence, user_emotion, comfortability, personality_emotions)
                print(robot_emotion)
                
                #robot_sentence, tone = generate_sentence(user_emotion, robot_emotion, user_sentence, personality_sentence, language_sentence, action)
                file_data={
                        "human_sentence":user_sentence,
                        "human_emotion":user_emotion,
                        "robot_emotion":robot_emotion,
                        "action": action
                }
                file.write(str(file_data))
                file.write("\n")
                file.flush()
                
                data_action["emotion"]=robot_emotion
                data_action["volume"]=mmap["volume"]
                data_action["gaze"]=mmap["gaze"]
                data_action["language_style"]=language_sentence
                data_action["action"]=action
                data_action["personality"]=personality
                print(data_action)
                resp=requests.post(url+'exec_actions', json=data_action, headers=headers)

        return True, action
        
    





        
