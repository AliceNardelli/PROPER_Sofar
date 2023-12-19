#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-
from head_movement import *
import time 
import threading
from animations import *
import random
import requests
import argparse
import socket
import os
import re
import zlib
import sys
import json
import xml
from map_sentences import *
from goal2_animations import *
from goal3_animations import *
from loc_functions import *
from flask import Flask, request, jsonify


       
url='http://127.0.0.1:5009/'
url1='http://127.0.0.1:5011/'
headers= {'Content-Type':'application/json'}

data = {
    "sentence": "p",
    "response":"q",
    "personality":""
}

data_sentence = {
    "activated": "p",
    "response":"q"
}

class Speak:

    def __init__(self,session):
        self.name="Pepper"
        self.session=session
        self.action=""
        self.personality=""
        self.parameters={}
        self.location=""
        self.set_pitch=False
        self.p=0
        self.ve=0
        self.vo=0
        self.tts2=self.session.service("ALMemory")
        self.tts4=self.session.service("ALSpeechRecognition")  
        self.touched=False
        self.m=self.session.service("ALMotion")
        self.traits="ac"
        self.grasp=False

        self.pitch={"low":0.83,
                    "mid":0.95,
                    "high":1.1,
                    }
        
        self.volume={"low":0.4,
                "mid":0.5,
                "dynamic":0.75,
                "very_dynamic":1,
            }
        
        self.velocity={"low":80,
                        "mid":90,
                        "rather_high":95,
                        "high":105,
                        }
        self.gaze(False,False)



    def add_gestures(self,to_say):
        #replace whit pauses
        print("-----------")
        to_say=to_say.replace("...",".")
        print(to_say)
        if self.grasp==False:
            signs=[".",",","!","?"]
            #signs=["."]
            #for s in signs:
                #indeces=[pos for pos, char in enumerate(to_say) if char == s]
            for pos, char in enumerate(to_say):
                    if char in signs:
                        if "e" in self.traits:
                            staff=speaking_motions_big[random.randrange(len(speaking_motions_big))]
                        elif "i" in self.traits:
                            staff=speaking_motions_small[random.randrange(len(speaking_motions_small))]
                        else:
                            staff=speaking_motions_medium[random.randrange(len(speaking_motions_medium))]
                        ind=to_say.index(char)
                        to_say=to_say[:(ind)] + " ^start("+staff+") " + char+ to_say[(ind+1):] 
                        ind=to_say.index(char)
                        if self.ve==80:
                            if char==",":
                                to_say=to_say[:(ind-1)]+" \\pau=400\\ "+to_say[(ind+1):]
                            else:
                                to_say=to_say[:(ind-1)]+" \\pau=800\\ "+to_say[(ind+1):]
                        elif self.ve==90:
                            if char==",":
                                to_say=to_say[:(ind-1)]+" \\pau=200\\ "+to_say[(ind+1):]
                            else:
                                to_say=to_say[:(ind-1)]+" \\pau=400\\ "+to_say[(ind+1):]
                        elif self.ve==95:
                            if char==",":
                                to_say=to_say[:(ind-1)]+" \\pau=150\\ "+to_say[(ind+1):]
                            else:
                                to_say=to_say[:(ind-1)]+" \\pau=350\\ "+to_say[(ind+1):]
                        elif self.ve==105:
                            if char==",":
                                to_say=to_say[:(ind-1)]+" \\pau=100\\ "+to_say[(ind+1):]
                            else:
                                to_say=to_say[:(ind-1)]+" \\pau=200\\ "+to_say[(ind+1):]           
                    
            if "e" in self.traits:
                staff=listening_motions_big[random.randrange(len(listening_motions_big))]
            elif "i" in self.traits:
                staff=listening_motions_small[random.randrange(len(listening_motions_small))]
            else:
                staff=listening_motions_medium[random.randrange(len(listening_motions_medium))]
            to_say=to_say+" ^start("+staff+") \\pau=200\\"
        else:    
            if self.ve==80:
                to_say=to_say.replace("."," \\pau=800\\ ").replace(","," \\pau=400\\ ")
            elif self.ve==90:
                to_say=to_say.replace("."," \\pau=400\\ ").replace(","," \\pau=200\\ ")
            elif self.ve==95:
                to_say=to_say.replace("."," \\pau=300\\ ").replace(","," \\pau=200\\ ")
            elif self.ve==105:
                to_say=to_say.replace("."," \\pau=200\\ ").replace(","," \\pau=100\\ ")
        print(to_say)
        return to_say  
    
    def hello(self):
        if "e" in self.traits:
            return hello_motions_big[random.randrange(len(hello_motions_big))]
        
        elif "i" in self.traits:
            return hello_motions_small[random.randrange(len(hello_motions_small))]
        
        else:
            return hello_motions_medium[random.randrange(len(hello_motions_medium))]
        

    def task(self):
        print(self.parameters["head"])
        if self.parameters["head"]=="tilt_down_shaking":
                tilt_down_shaking(self.session)
        elif self.parameters["head"]=="tilt_up_shaking":
                tilt_up_shaking(self.session)
        elif self.parameters["head"]=="nodding":
                nodding(self.session)
        elif self.parameters["head"]=="shaking_low":
                shaking_low(self.session)
        elif  self.parameters["head"]=="shaking":
                big_shaking(self.session)
        else:
                print("no head movement")
        print("executing head motion")


    
    def gaze(self,boolean,boolean2):
        ab=self.session.service("ALAutonomousBlinking")
        ab.setEnabled(boolean)
        abm=self.session.service("ALBackgroundMovement")
        abm.setEnabled(boolean)
        aba=self.session.service("ALBasicAwareness")
        aba.setEnabled(boolean2)
        alm=self.session.service("ALSpeakingMovement")
        alm.setMode("contextual")
        alm.setEnabled(False)
        asm=self.session.service("ALListeningMovement")
        asm.setEnabled(boolean)

    def touch_detected(self,value): #esempio di callback
        self.touched=True
        print("touched")
        time.sleep(1)
        
    def executing(self,anim_speech_service):
        try:
           sentence_action=mmap_action_sentences[self.action][0]
           behavior=mmap_action_sentences[self.action][1]
           #call the service to ask the question
        except:
           sentence_action=self.action.replace("_"," ").lower()
           behavior=""
           #call the service to ask the question 
        if self.action=="say_greetings" :
                h=self.hello()
                to_say=" ^start("+h+") \\pau=2000\\"
                anim_speech_service.say(to_say) 
        data["language"]=self.parameters["language"]
        data["sentence"]=sentence_action
        data["personality"]=self.personality
        print(data)
        print("--------------------------")
        
        resp=requests.put(url+'sentence_generation', json=data, headers=headers)
        to_say=eval(resp.text)["response"]
        print(to_say)
        
        thread = threading.Thread(target=self.task)
        thread.start()
        to_say=self.add_gestures(to_say)
        anim_speech_service.say(to_say) 
        thread.join()
        
        print("Executing behavior ", behavior)
        if behavior=="tablet":
            tablet(self.session, mmap_action_sentences[self.action][2])

        elif behavior=="bring_candy":
            to_say="Toccami la testa quando la caramella sarà nella mia mano"
            thread = threading.Thread(target=self.task)
            thread.start()
            to_say=self.add_gestures(to_say)
            anim_speech_service.say(to_say) 
            thread.join()
            ask_pick_sweet(self.session)
        
        elif behavior=="breathe":
            breath(self.session, anim_speech_service)

        elif behavior=="curl_movement":
            curl(self.session, anim_speech_service)

        elif behavior=="curl_blink":
            blink(session, 6, 1, "green")

        elif behavior=="yoga":
            if self.personality=="Introvert":
                reps=3
                velocity="low"
            elif self.personality=="Extrovert":
                 reps=6
                 velocity="high"
            elif self.personality=="Conscientous":
                 reps=6
                 velocity="mid"
            elif self.personality=="Unscupolous":
                 reps=2
                 velocity="mid"
            else:
                reps=4
                velocity="mid"
            yoga(self.session,velocity,reps)

        elif behavior=="get_away":
            #nav(session,x,y,yaw,vel,prox):
            nav(self.session,-0.5,0,0,0.2,0.05)

        elif behavior=="embrace":
             embrace(self.session)
        
        elif behavior=="high_five":
            high_five(self.session)

        if "ask" in to_say:
            data_sentence["activated"]="True"
            resp=requests.put(url1+'listener', json=data_sentence, headers=headers)
            human_sentence=eval(resp.text)["response"]
            data["language"]=self.parameters["language"]
            data["sentence"]=human_sentence
            data["personality"]=self.personality
            resp=requests.put(url+'sentence_response', json=data, headers=headers)
            to_say=eval(resp.text)["response"]
            print(to_say)
            thread = threading.Thread(target=self.task)
            thread.start()
            to_say=self.add_gestures(to_say)
            anim_speech_service.say(to_say) 
            thread.join()
             

    def set_params(self):
        #set all the autonomous capability to disabled
        self.gaze(False,False)
        #If the gaze is mutual enable tracking
        name_led="FaceLeds"
        leds=self.session.service("ALLeds")
        leds.reset(name_led)
        tts = self.session.service("ALTextToSpeech")
        speak_move_service = self.session.service("ALSpeakingMovement")
        tts.setLanguage("Italian") 
        
        if self.set_pitch==False:
            # at the first interaction set speaking parameters
            self.vo=self.volume[self.parameters["volume"]]
            self.p=self.pitch[self.parameters["pitch"]]
            self.ve=self.velocity[self.parameters["velocity"]]
            self.set_pitch=True
        #setting parameters
        tts.setVolume(self.vo) 
        tts.setParameter("pitchShift",self.p)
        tts.setParameter("speed",self.ve)  
        time.sleep(1) 
        anim_speech_service = self.session.service("ALAnimatedSpeech") 
        print("params voice set")
        #executing the behavior
        self.executing(anim_speech_service)
        #stop tracking
        """
        if self.parameters["gaze"]=="mutual":
            tracker.stopTracker()
        """

    def speak(self,action,personality,params):  
        print(action,personality)        
        self.action=action.split(" ")[0]
        self.personality=personality
        self.parameters=params
        self.set_params()

        
        
