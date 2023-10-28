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
from flask import Flask, request, jsonify
from sentences_festival import festival_dict_halloween

       
url='http://127.0.0.1:5009/'
headers= {'Content-Type':'application/json'}

data = {
    "sentence": "p",
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
        self.topics=["Cibo","Sport","Vacanze","Tempo libero","Musica","Religione"]
        self.counter=0 #change0
        self.colors=["red","orange","yellow","green","blu","purple"]
        self.ins=[0,1,2,3,6,7]
        self.traits=""
        self.grasp=False
        self.sentences_dict={ "s":festival_dict_halloween,
                              }
        
     

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
        set_of_sentences=self.sentences_dict["s"]
        ss=set_of_sentences[self.action]
        if self.action=="s1" :
                h=self.hello()
                to_say=" ^start("+h+") \\pau=2000\\"
                print(to_say)
                anim_speech_service.say(to_say) 
        
        if self.action=="s6" :
            img="sweet.png"
            self.tablet(img)        
        
        if  type(ss)==list:
            #ask to chatgpt the sentence to say
            to_say=ss[random.randrange(len(ss))]
            thread = threading.Thread(target=self.task)
            # run the thread
            thread.start()
            to_say=self.add_gestures(to_say)
            anim_speech_service.say(to_say) 
            # wait for the thread to finish
            print('Waiting for the thread...')
            thread.join()

        if self.action=="s4" or self.action=="s5" or self.action=="s6" or self.action=="s7" or self.action=="s8" or self.action=="s9" or self.action=="s10":
            self.give_take_object_touch(1,1)
            self.grasp_object()
            time.sleep(3)
            self.ask_pose_block(ss,anim_speech_service) 
        #TABLET IMMAGINI


    def ask_pose_block(self,ss,anim_speech_service): 
            if "d" in self.traits:#rude
                self.give_take_object(0) 
                self.throw_object()   
            else:
                self.give_take_object(1) 
                 

   
    def tablet(self,im):
        DEF_IMG_APP = "tablet_images"
        TABLET_IMG_DEFAULT = im
        #TABLET_IMG_DEFAULT = "police_logo.png"
        sTablet = self.session.service("ALTabletService")
        image_dir = "http://%s/apps/%s/img/" % (sTablet.robotIp(), DEF_IMG_APP)
        tablet_image = image_dir + TABLET_IMG_DEFAULT
        print(tablet_image)
        sTablet.showImage(tablet_image)
        raw_input("Press Enter to continue...")
        sTablet.hideImage()

    def grasp_object(self):
        m=self.session.service("ALMotion")
        frac_speed=0.5
        chain=["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"]
        t=0
        angle=[-0.1 ,0.5,-1.56,-0.0,-1.7,0]
        stiff=len(chain)*[1]
        m.setStiffnesses(chain,stiff)
        while t<3:
            m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
            time.sleep(1)
            t+=1
        t=0
        stiff=len(chain)*[0]
        m.setStiffnesses(chain,stiff)

    def give_take_object_touch(self,hand,stiffness):
        m=self.session.service("ALMotion")
        frac_speed=0.5
        angle0=[-0.1 ,0.5,-1.56,-0.0,-1.7,0]
        angle=[-0.1 ,0.5,-1.56,-0.0,-1.7,hand]
        chain=["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"]
        t=0
        stiff=len(chain)*[1]
        m.setStiffnesses(chain,stiff)
        m.angleInterpolationWithSpeed(chain,angle0,frac_speed)
        self.touched=False
        touch = self.tts2.subscriber("MiddleTactilTouched") #questo permette la callback
        connection = touch.signal.connect(self.touch_detected) #segnale della sottoscrizione
        while self.touched==False:
            m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
            time.sleep(1)
            print("Hand open")
            t+=1
        self.touched=False
        stiff=len(chain)*[stiffness]
        m.setStiffnesses(chain,stiff)
    
    def callback(self, x, y):
            self.touched=True

    def give_take_object(self,hand):
        print("Give take the obj")
        m=self.session.service("ALMotion")
        frac_speed=0.5
        angle=[-0.1 ,0.5,-1.56,-0.0,-1.7,hand]
        chain=["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"]
        t=0
        stiff=len(chain)*[1]
        m.setStiffnesses(chain,stiff)
        while t<3:
            m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
            time.sleep(1)
            t+=1
        stiff=len(chain)*[0]
        m.setStiffnesses(chain,stiff)


    def throw_object(self):
        print("Throw obj")
        m=self.session.service("ALMotion")
        frac_speed=0.5
        angle=[-0.1 ,0.5,-0.0,-0.0,-0.0,1]
        chain=["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"]
        stiff=len(chain)*[1]
        m.setStiffnesses(chain,stiff)
        t=0
        while t<3:
            m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
            t+=1
        stiff=len(chain)*[0]
        m.setStiffnesses(chain,stiff)


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
            #self.set_pitch=True
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

        
        
