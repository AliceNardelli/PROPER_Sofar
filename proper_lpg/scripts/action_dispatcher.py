#!/usr/bin/env python
import os
import shutil
import subprocess
import json
import time
import numpy as np
from proper_lpg.srv import PersonalityGenerator, PersonalityGeneratorRequest
from proper_lpg.srv import ExecAction, ExecActionResponse
from pp_task.srv import MoveArm, MoveArmRequest
from std_msgs.msg import String
import rospy
from proper_lpg.get_parameters import *
import requests
from gtts import gTTS 
import pygame
emotion=""
attention=""
headers= {'Content-Type':'application/json'}

url='http://127.0.0.1:5018/'
data={
    "emotion":"",
    "action":"",
    "response_style":"",
    "selected_personality":"",
    "limit_response":"",
    "response":"",
}
map_action={
    "say_human_voice_turn1":"pass the turn",
    "say_human_voice_turn2":"pass the turn", 
}

map_perception_emotion={
   "A_SA":["Attentive","Sad"],
   "NA_SA":["Distracted","Sad"],
   "NA_SU":["Distracted","Surprise"],
   "A_SU":["Attentive","Surprise"],
   "NA_H":["Distracted","Happy"],
   "A_H":["Attentive","Happy"],
   "NA_A":["Distracted","Anger"],
   "A_A":["Attentive","Anger"],
   "NA_D":["Distracted","Disgust"],
   "A_D":["Attentive","Disgust"],
   "NA_F":["Distracted","Fear"],
   "A_F":["Attentive","Fear"],
   "NA_N":["Distracted","Neutral"],
   "A_N":["Attentive","Neutral"],
}

volume_map={
    "no_active":0,
    "low":0.1,
    "mid":0.4,
    "dynamic":0.8,
    "very_dynamic":1,
}

g_speed={
    "no_active":0.5,
    "low":0.5,
    "mid":0.8,
    "high":1,
}

def callback(data):
    global emotion, attention
    emotion=map_perception_emotion[data.data][1]
    attention=map_perception_emotion[data.data][0]
    

def save_file(text):
    tts = gTTS(text=text, lang='it', slow=False)
    tts.save("temp.mp3")
    print("tutto fatto, file salvato!")
    return "temp.mp3"

def reproduce_audio(file_name,volume):
    pygame.init()
    sp=pygame.mixer.Sound(file_name)
    length=sp.get_length()
    sp.set_volume(volume)
    sp.play()
    time.sleep(length)


def dispatch_action(req):
    global robot_block, human_block, emotion, attention
    try:
        rospy.wait_for_service('personality_generator_srv')
        personality_generator_srv = rospy.ServiceProxy('personality_generator_srv', PersonalityGenerator)
        msg=PersonalityGeneratorRequest()
        msg.action=req.action.split("_")[0]
        msg.personality=req.personality
        resp = personality_generator_srv(msg)     
        mmap =get_map(resp.params)
        #SPEAK ACTION
        print(req.action)
        if mmap["language"]!="no_active":
            print("I am here")
            if "say_human" in  str(req.action):
                human_block+=1
            if "tablet" in req.action:
                file="/home/alice/bepp.mp3"
            else:
                print("I am here2")
                data["emotion"]=emotion
                data["attention"]=attention
                data["response_style"]=mmap["language"]
                if msg.personality=="Unscrupolous":
                    data["selected_personality"]="Distracted"
                else:
                    data["selected_personality"]=msg.personality
                try:
                    data["action"]=map_action[req.action]
                except:
                    data["action"]=req.action.replace("_"," ")
                resp=requests.put(url+'run_completion', json=data, headers=headers)
                print("I am here3")
                file=save_file(eval(resp.text)["response"])
            vol=volume_map[mmap["volume"]]
            reproduce_audio(file,vol)
            return True
        #MOVE ACTION
        else:
            print("EXEC "+ str(req.action))
            if "pick_place" in  str(req.action):
                req2=MoveArmRequest()
                if "replace" in  str(req.action):
                    
                    req2.block=human_block
                    req2.block_owner="human"
                    human_block+=1
                else:
                    
                    req2.block=robot_block
                    req2.block_owner="robot"
                    robot_block+=1
                if "wrong" in  str(req.action):
                    req2.style="wrong"
                else:
                    req2.style="precise"
                req2.final_pose=req.move
                req2.amplitude=mmap["amplitude"]
                req2.speed=g_speed[mmap["g_speed"]]
                print(req2)
                rospy.wait_for_service('/kinova_move_srv')
                kinova_srv = rospy.ServiceProxy('/kinova_move_srv', MoveArm)
                resp = kinova_srv(req2) 
                if "wrong" in  str(req.action):
                    msg=PersonalityGeneratorRequest()
                    msg.action="ask"
                    msg.personality=req.personality
                    resp = personality_generator_srv(msg)     
                    mmap =get_map(resp.params)
                    data["emotion"]=emotion
                    data["attention"]=attention
                    data["response_style"]=mmap["language"]
                    if msg.personality=="Unscrupolous":
                        data["selected_personality"]="Distracted"
                    else:
                        data["selected_personality"]=msg.personality

                    data["action"]="ask the human to correctly put the block because you make an error bu you are lazy to pick again the block"
                    resp=requests.put(url+'run_completion', json=data, headers=headers)
                
                    file=save_file(eval(resp.text)["response"])
                    vol=volume_map[mmap["volume"]]
                    reproduce_audio(file,vol)

                return True
            
            else:
                req2=MoveArmRequest()
                if "home" in str(req.action):
                    req2.block_owner="home"
                else:
                    req2.block_owner="random"
                rospy.wait_for_service('/kinova_move_srv')
                kinova_srv = rospy.ServiceProxy('/kinova_move_srv', MoveArm)
                resp = kinova_srv(req2) 
                return True
            
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
    #execute 
    return True

if __name__ == "__main__":
    global robot_block, human_block
    robot_block=0
    human_block=0
    rospy.Subscriber("perception", String, callback)
    rospy.init_node('action_dispatcher')
    s = rospy.Service('action_dispatcher_srv', ExecAction, dispatch_action)
    print("Ready to add two ints.")
    rospy.spin()




        
