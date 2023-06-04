from head_movement import *
import time 
from time import sleep
import threading
from speaking_dictionary_italian import *
import random
import requests
#http://doc.aldebaran.com/2-4/naoqi/audio/altexttospeech-tuto.html#tag-tutorial trial to see paw and if setting parameters via tts


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
        self.blocks=["yellow","green","red","blue","yellow","purple"]
        self.counter=0

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
        ss=sentence_generation[self.action]
        if "behavior" in ss:
            if ss=="behavior1":
                self.chit_chat(ss,anim_speech_service)  
            if ss=="behavior2" or ss=="behavior3" or ss=="behavior10" or ss=="behavior11":
                self.present_task(ss,anim_speech_service)
            if ss=="behavior4" or ss=="behavior5":
                self.ask_pick_block(ss,anim_speech_service)
            if ss=="behavior6" or ss=="behavior7" or ss=="behavior8" or ss=="behavior9":
                self.ask_pose_block(ss,anim_speech_service)      
        else:
            #ask to chatgpt the sentence to say
            ways=modality[self.personality]
            way_1=ways.pop(random.randint(0,len(ways)-1))
            way_2=ways.pop(random.randint(0,len(ways)-1))
            to_generate=sentence.replace("way_1",way_1).replace("way_2",way_2)+"'"+ss+"'"
            data["sentence"]=to_generate
            resp=requests.put(url+'sentence_generation', json=data, headers=headers)
            to_say=eval(resp.text)["response"]
            thread = threading.Thread(target=self.task)
            # run the thread
            thread.start()
            anim_speech_service.say(to_say) 
            # wait for the thread to finish
            print('Waiting for the thread...')
            thread.join()
               
    def chit_chat(self,ss,anim_speech_service):
        ways=modality[self.personality]
        way_1=ways.pop(random.randint(0,len(ways)-1))
        way_2=ways.pop(random.randint(0,len(ways)-1))
        sentences=behaviors[ss]
        topic=self.topics[random.randint(0,len(self.topics)-1)]
        s1=sentences[0].replace("*",topic).replace("way_1",way_1).replace("way_2",way_2)
        data["sentence"]=s1
        resp=requests.put(url+'sentence_generation', json=data, headers=headers)
        to_say=eval(resp.text)["response"]
        thread = threading.Thread(target=self.task)
        thread.start()
        anim_speech_service.say(to_say)
        thread.join()
        for i in range(3):
           #LISTEN A REPLY
           reply=""
           ways=modality[self.personality]
           way_1=ways.pop(random.randint(0,len(ways)-1))
           way_2=ways.pop(random.randint(0,len(ways)-1))
           s2=sentences[1].replace("+",topic).replace("*",reply).replace("way_1",way_1).replace("way_2",way_2)
           data["sentence"]=s2
           resp=requests.put(url+'sentence_generation', json=data, headers=headers)
           to_say=eval(resp.text)["response"]
           thread = threading.Thread(target=self.task)
           thread.start()
           anim_speech_service.say(to_say)
           thread.join()

    def present_task(self,ss,anim_speech_service):
        sentences=behaviors[ss]
        for s in sentences:
            ways=modality[self.personality]
            way_1=ways.pop(random.randint(0,len(ways)-1))
            way_2=ways.pop(random.randint(0,len(ways)-1))
            to_generate=sentence.replace("way_1",way_1).replace("way_2",way_2)+"'"+s+"'"
            data["sentence"]=to_generate
            resp=requests.put(url+'sentence_generation', json=data, headers=headers)
            to_say=eval(resp.text)["response"]
            thread = threading.Thread(target=self.task)
            thread.start()
            anim_speech_service.say(to_say)
            thread.join()

    def ask_pick_block(self,ss,anim_speech_service):
        sentences=behaviors[ss] 
        color=self.blocks[self.counter]
        self.counter+=1
        s=sentences[random.randint(0,len(sentences)-1)]
        s=s.replace("*",color)
        if ss=="behavior4":#voice
            s2=[s,"Touch me the head when you have put the block in my hand"]
            for s1 in s2:
                ways=modality[self.personality]
                way_1=ways.pop(random.randint(0,len(ways)-1))
                way_2=ways.pop(random.randint(0,len(ways)-1))
                to_generate=sentence.replace("way_1",way_1).replace("way_2",way_2)+"'"+s1+"'"
                data["sentence"]=to_generate
                resp=requests.put(url+'sentence_generation', json=data, headers=headers)
                to_say=eval(resp.text)["response"]
                thread = threading.Thread(target=self.task)
                thread.start()
                anim_speech_service.say(to_say)
                thread.join()
            self.give_take_object_touch(1)
            self.grasp_object()
               
        else:#tablet 
            #s2=[s,"Please touch the tablet when you have put the block in my hand"]
            #for s1 in s2:
            #msg=sentence[0]+modality[self.personality]+sentence[1]+s1
            #send the msg to chatgpt
            thread = threading.Thread(target=self.task)
            thread.start()
            self.tablet(color)
            thread.join()  
            self.give_take_object_tablet(1)
            self.grasp_object()     
        
    def ask_pose_block(self,ss,anim_speech_service):
        sentences=behaviors[ss] 
        color=self.blocks[self.counter-1]
        s=sentences[random.randint(0,len(sentences)-1)]
        s=s.replace("*",color)
        if ss=="behavior6" or ss=="behavior7":#voice
            s2=[s,"Touch me the head when you have put the block in my hand"]
            for s1 in s2:
                ways=modality[self.personality]
                way_1=ways.pop(random.randint(0,len(ways)-1))
                way_2=ways.pop(random.randint(0,len(ways)-1))
                to_generate=sentence.replace("way_1",way_1).replace("way_2",way_2)+"'"+s1+"'"
                data["sentence"]=to_generate
                resp=requests.put(url+'sentence_generation', json=data, headers=headers)
                to_say=eval(resp.text)["response"]
                thread = threading.Thread(target=self.task)
                thread.start()
                anim_speech_service.say(to_say)
                thread.join()
            if self.personality!="Disagreeable":
                self.give_take_object(0)
            if ss=="behavior7": #gently
                self.give_take_object_touch(1) 
            else:#rude
                self.give_take_object(1) 
                self.throw_object()
        else:#tablet
            thread = threading.Thread(target=self.task)
            thread.start()
            self.tablet(color)
            thread.join() 
            if self.personality!="Disagreeable":
             self.give_take_object(0) 
            if ss=="behavior9": #gently
                self.give_take_object_tablet(1)#wait until human touch
            else:#rude
                self.give_take_object(1)
                self.throw_object()

    def tablet(self,color):
        DEF_IMG_APP = "tablet_images"
        #TABLET_IMG_DEFAULT = color+".png"
        TABLET_IMG_DEFAULT = "police_logo.png"
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
        while t<5:
            m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
            time.sleep(1)
            t+=1
        t=0
        stiff=len(chain)*[0]
        m.setStiffnesses(chain,stiff)

    def give_take_object_touch(self,hand):
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
        stiff=len(chain)*[0]
        m.setStiffnesses(chain,stiff)
    
    def callback(self, x, y):
            self.touched=True

    def give_take_object_tablet(self,hand):
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
            stiff=len(chain)*[0]
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
        while t<5:
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
        while t<5:
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



"""
    def execute(self,a,anim_speech_service):  
        #try:
            sentences=self.df.loc[self.df.action==a]
            print("-------------")
            print(sentences)
            print("-------------")
            for index,row in sentences.iterrows():
                print(a)
                anim_speech_service.say(row.response) 
                if row.action=="talk":
                    #self.tts4.setLanguage("Italian")
                    self.tts4.setAudioExpression(True)
                    #tts4.setVocabulary(["no", "si","bene","finito"], False)
                    print("------LISTENING------------")
                    self.tts4.subscribe("WordRecognized")
                    time.sleep(3)
                    answ=self.tts2.getData("WordRecognized")
                    print(answ)
                    self.tts4.unsubscribe("WordRecognized")
                    print("------ANSWER-----------")
                elif row.action=="ask to order tower":
                            print("there")
                            self.touched=False
                            #self.al.setState("solitary")
                            #self.al.stopAll() 
                            
                            touch = self.tts2.subscriber("MiddleTactilTouched") #questo permette la callback
                            connection = touch.signal.connect(self.touch_detected) #segnale della sottoscrizione
                            while self.touched==False:
                                print("while")
                                time.sleep(1)
                            self.touched=False
                            #self.al.setState(self.autonomouslife)
                    
        #except:
             #anim_speech_service.say("Non posso eseguire azioni")"""
        
        
