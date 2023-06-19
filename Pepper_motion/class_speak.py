#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-
from head_movement import *
import time 
import threading
from animations import *
from extrovert import *
from disagreeable import *
from ed import *
from ic import *
from au import *
from id import *
from eu import *
from iu import *
from ia import *
from ec import *
from ea import *
from dc import *
from du import *
from ac import *
import random
import requests

from cairlib.DialogueStatistics import DialogueStatistics
from cairlib.DialogueState import DialogueState
from cairlib.DialogueTurn import DialogueTurn
from cairlib.CAIRclient_utils import Utils
import xml.etree.ElementTree as ET
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
        self.counter=0
        self.colors=["red","orange","yellow","green","red","orange"]
        self.ins=[0,1,2,3,6,7]
        self.traits="ia"
        self.grasp=False
        self.sentences_dict={ "Extrovert":sentence_generation_extroverted,
                              "Disagreeable":sentence_generation_disagreeable,
                              "ed":sentence_generation_ed,
                              "ic":sentence_generation_ic,
                              "au":sentence_generation_au,
                              "id":sentence_generation_id,
                              "eu":sentence_generation_eu,
                              "iu":sentence_generation_iu,
                              "ia":sentence_generation_ia,
                              "ec":sentence_generation_ec,
                              "ea":sentence_generation_ea,
                              "dc":sentence_generation_dc,
                              "du":sentence_generation_du,
                              "ac":sentence_generation_ac,}
        
        self.behaviors_dict={
            "Extrovert":behaviors_e,
            "Disagreeable":behaviors_d,
            "ed":behaviors_ed,
            "ic":behaviors_ic,
            "au":behaviors_au,
            "id":behaviors_id,
            "eu":behaviors_eu,
            "iu":behaviors_iu,
            "ia":behaviors_ia,
            "ec":behaviors_ec,
            "ea":behaviors_ea,
            "dc":behaviors_dc,
            "du":behaviors_du,
            "ac":behaviors_ac,
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


    def dialogue(self):
        # Location of the server
        cineca = "131.175.205.146"
        #local = "130.251.13.118"
        local="127.0.0.1"
        server_ip = cineca
        audio_recorder_ip = local
        registration_ip = local
        port = "5000"
        BASE = "http://" + cineca + ":" + port + "/CAIR_hub"
        min_registered_users_number = 1
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Try to connect to the socket that listens to the user speech
        try:
            print("Attempting to connect to the socket...")
            client_socket.connect((audio_recorder_ip, 9090))
            print("socket connected")
        except ConnectionError:
            print("Check socket connection with audio_recorder.py")
            sys.exit(1)

        utils = Utils("it", server_ip, registration_ip, port)
        # Retrieve the states of the users
        with open("/home/alice/CAIRclient/client_multiparty/dialogue_state.json") as f:
            dialogue_state = DialogueState(d=json.load(f))
            print("dialoge state opened")
        
        # Tell the audio recorder that the client is ready to receive the user reply
        client_socket.send(dialogue_state.sentence_type.encode('utf-8'))
        print("sent")
        xml_string = client_socket.recv(1024).decode('utf-8')
        print("received")
        if xml_string == "":
                print("Socket error")
                sys.exit(1)

        # Do not proceed until the xml string is complete and all tags are closed
        proceed = False
        while not proceed:
                try:
                    tree=ET.ElementTree(ET.fromstring(xml_string))
                    proceed = True
                except xml.etree.ElementTree.ParseError:
                    # If the xml is not complete, read again from the socket
                    print("The XML is not complete.")
                    xml_string = xml_string + client_socket.recv(1024).decode('utf-8')

        sentence = str(tree.findall('profile_id')[0].text)
        print(sentence)
        return sentence
    
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
                to_say=to_say.replace(".","\\pau=800\\").replace(",","\\pau=400\\")
            elif self.ve==90:
                to_say=to_say.replace(".","\\pau=400\\").replace(",","\\pau=200\\")
            elif self.ve==95:
                to_say=to_say.replace(".","\\pau=300\\").replace(",","\\pau=200\\")
            elif self.ve==105:
                to_say=to_say.replace(".","\\pau=200\\").replace(",","\\pau=100\\")
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
        set_of_sentences=self.sentences_dict[self.traits]
        ss=set_of_sentences[self.action]
        if ("speak_about" in self.action) and (self.grasp==False) :
                h=self.hello()
                to_say=" ^start("+h+") \\pau=2000\\"
                print(to_say)
                anim_speech_service.say(to_say) 
                

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
            if  ("say_goodbye" in self.action) and (self.grasp==False):
                   h=self.hello()
                   to_say=" ^start("+h+") \\pau=2000\\"
                   anim_speech_service.say(to_say) 
                   
        else:
            if ss=="behavior1":
                self.chit_chat(ss,anim_speech_service)  
            if ss=="behavior2" or ss=="behavior3":
                self.present_task(ss,anim_speech_service)
            if ss=="behavior4" or ss=="behavior5":
                self.ask_pick_block(ss,anim_speech_service)
            if ss=="behavior6" or ss=="behavior7" or ss=="behavior8" or ss=="behavior9":
                self.ask_pose_block(ss,anim_speech_service) 
      
    def chit_chat(self,ss,anim_speech_service):
        ways=modality[self.personality]
        way_1=ways[random.randint(0,len(ways)-1)]
        way_2=ways[random.randint(0,len(ways)-1)]
        b=self.behaviors_dict[self.traits]
        sentences=b[ss]
        topic=self.topics[random.randint(0,len(self.topics)-1)]
        s1=sentences[0].replace("*",topic).replace("way_1",way_1).replace("way_2",way_2)
        data["sentence"]=s1
        resp=requests.put(url+'sentence_generation', json=data, headers=headers)
        to_say=eval(resp.text)["response"]
        thread = threading.Thread(target=self.task)
        thread.start()
        to_say=self.add_gestures(to_say)
        anim_speech_service.say(to_say)
        thread.join()
        for i in range(3):
           print("before getting audio")
           reply=self.dialogue()
           way_1=ways[random.randint(0,len(ways)-1)]
           way_2=ways[random.randint(0,len(ways)-1)]
           print("after getting audio")
           print(reply)
           s2=sentences[1].replace("+",topic).replace("*",reply).replace("way_1",way_1).replace("way_2",way_2)
           data["sentence"]=s2
           resp=requests.put(url+'sentence_generation', json=data, headers=headers)
           to_say=eval(resp.text)["response"]
           thread = threading.Thread(target=self.task)
           thread.start()
           to_say=self.add_gestures(to_say)
           anim_speech_service.say(to_say)
           thread.join()
        thread = threading.Thread(target=self.task)
        thread.start()
        time.sleep(3)
        if "u" in self.traits:
            to_say=self.add_gestures("Proviamo a non distrarci e continuiamo a lavorare")
        elif "e" in self.traits:
            to_say=self.add_gestures("è bellissimo chiaccherare con te ma è ora di tornare a lavorare")
        anim_speech_service.say(to_say)
        thread.join()

    def present_task(self,ss,anim_speech_service):
        b=self.behaviors_dict[self.traits]
        sentences=b[ss]
        for s in sentences:
            to_say=s
            thread = threading.Thread(target=self.task)
            thread.start()
            to_say=self.add_gestures(to_say)
            anim_speech_service.say(to_say)
            thread.join()

    def ask_pick_block(self,ss,anim_speech_service):
        b=self.behaviors_dict[self.traits]
        sentences=b[ss] 
        s=sentences[self.ins[self.counter]]
        if ss=="behavior4":#voice
            s2=[s,"Toccami la testa quando avrai messo il cubetto nella mia mano"]
            for s1 in s2:
                thread = threading.Thread(target=self.task)
                thread.start()
                to_say=self.add_gestures(s1)
                anim_speech_service.say(to_say)
                self.grasp=True
                thread.join()
            self.give_take_object_touch(1,1)
            self.grasp_object() 

        else:#tablet 
            thread = threading.Thread(target=self.task)
            thread.start()
            image="pick_"+self.colors[self.counter]+".png"
            self.tablet(image)
            thread.join()  
            self.grasp=True
            self.give_take_object_tablet(1,1)
            self.grasp_object()     
        
    def ask_pose_block(self,ss,anim_speech_service):
        b=self.behaviors_dict[self.traits]
        sentences=b[ss] 
        s=sentences[self.ins[self.counter]]
        
        if ss=="behavior6" or ss=="behavior7":#voice
            s2=[s,"Toccami la testa quando avrai preso il blocchetto"]
            thread = threading.Thread(target=self.task)
            thread.start()
            to_say=self.add_gestures(s2[0])
            anim_speech_service.say(to_say)
            thread.join()    
            if "a" in self.traits: #gently
                thread = threading.Thread(target=self.task)
                thread.start()
                to_say=self.add_gestures(s2[1])
                anim_speech_service.say(to_say)
                thread.join()
                self.give_take_object_touch(1,0) 
            elif "d" in self.traits:#rude
                rnd=random.randint(0,2)
                if rnd==0:
                    self.give_take_object(0) 
                    self.throw_object()
                else:
                    self.give_take_object(1)
            else:
                rnd=random.randint(0,2)
                if rnd==0:
                    self.give_take_object(0) 
                    self.throw_object()
                else:
                    thread = threading.Thread(target=self.task)
                    thread.start()
                    to_say=self.add_gestures(s2[1])
                    anim_speech_service.say(to_say)
                    thread.join()
                    self.give_take_object_touch(1,0) 
            self.grasp=False
            
        else:#tablet
            thread = threading.Thread(target=self.task)
            thread.start()
            image="put_"+self.colors[self.counter]+".png"
            self.tablet(image)
            thread.join() 
            if "a" in self.traits: #gently
                self.give_take_object_tablet(1,0) 
            elif "d" in self.traits:#rude
                rnd=random.randint(0,2)
                if rnd==0:
                    self.give_take_object(0) 
                    self.throw_object()
                else:
                    self.give_take_object(1)
                tabletService = self.session.service("ALTabletService")
                tabletService.hideImage()
            else:
                rnd=random.randint(0,2)
                if rnd==0:
                    self.give_take_object(0) 
                    self.throw_object()
                    tabletService = self.session.service("ALTabletService")
                    tabletService.hideImage()
                else:
                    self.give_take_object_tablet(1,0)
            self.grasp=False

        self.counter+=1
   
    def tablet(self,im):
        DEF_IMG_APP = "tablet_images"
        TABLET_IMG_DEFAULT = im
        #TABLET_IMG_DEFAULT = "police_logo.png"
        sTablet = self.session.service("ALTabletService")
        image_dir = "http://%s/apps/%s/img/" % (sTablet.robotIp(), DEF_IMG_APP)
        tablet_image = image_dir + TABLET_IMG_DEFAULT
        print(tablet_image)
        sTablet.showImage(tablet_image)
        time.sleep(3)

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
        angle=[-0.1 ,0.5,-1.56,-0.0,-1.7,hand]
        chain=["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"]
        t=0
        stiff=len(chain)*[1]
        m.setStiffnesses(chain,stiff)
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

    def give_take_object_tablet(self,hand,stiffness):
            m=self.session.service("ALMotion")
            frac_speed=0.5
            angle=[-0.1 ,0.5,-1.56,-0.0,-1.7,hand]
            chain=["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"]
            t=0
            stiff=len(chain)*[1]
            m.setStiffnesses(chain,stiff)
            self.touched=False
            tabletService = self.session.service("ALTabletService")
            signalID = tabletService.onTouchDown.connect(self.callback)
            while self.touched==False:
                m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
                time.sleep(1)
                print("Hand open")
                t+=1
            self.touched=False
            stiff=len(chain)*[stiffness]
            m.setStiffnesses(chain,stiff)
            tabletService.hideImage()

            
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
        if self.parameters["gaze"]=="mutual":
            tracker=self.session.service("ALTracker")
            tracker.track("Face")
        else:
            print("no tracking")

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
        if self.parameters["gaze"]=="mutual":
            tracker.stopTracker()

    def speak(self,action,personality,params):  
        print(action,personality)        
        self.action=action.split(" ")[0]
        self.personality=personality
        self.parameters=params
        self.set_params()

        
        
