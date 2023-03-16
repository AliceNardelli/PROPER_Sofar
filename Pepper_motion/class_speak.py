from head_movement import *
import time 
from time import sleep
import threading



class Speak:

    def __init__(self,session):
        self.name="Pepper"
        self.session=session
        self.action=""
        self.personality=""
        self.parameters={}
        self.action_say=["say welcome","speak about rules", "ask to order tower","talk","say goodbye"]
        self.location=""
        self.set_pitch=False
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
                        "rather_high":105,
                        "high":110,
                        }
        
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

    def gaze(self,boolean):
        al=self.session.service("ALAutonomousLife")
        if boolean:
            al.setState("interactive")
        else:
            al.setState("solitary") #solitary
            al.stopAll()
        ab=self.session.service("ALAutonomousBlinking")
        ab.setEnabled(boolean)
        abm=self.session.service("ALBackgroundMovement")
        abm.setEnabled(boolean)
        aba=self.session.service("ALBasicAwareness")
        aba.setEnabled(boolean)
        alm=self.session.service("ALSpeakingMovement")
        alm.setEnabled(boolean)
        asm=self.session.service("ALSpeakingMovement")
        asm.setEnabled(boolean)
        awr = self.session.service("ALBasicAwareness")
        awr.setEnabled(boolean)

    def execute(self,a,anim_speech_service):
        if a=="say welcome":
            anim_speech_service.say("Buongiorno Mi chiamo Pepper")
        elif a=="speak about rules":
            anim_speech_service.say("Devi ordinare i cubetti")
        elif a=="ask to order tower":
            anim_speech_service.say("Metti quello rosso e poi quello blu")
        elif a=="talk":
            anim_speech_service.say("Ti piace la musica?")
        elif a=="say goodbye":
            anim_speech_service.say("Arrivederci")
        else:
           anim_speech_service.say("Non posso esegure azioni")
        time.sleep(3)

        
    def set_params(self):
        #par={i:self.parameters[i] for i in self.parameters if self.parameters[i]!="no_active"}
        
        print(self.parameters)
        if self.parameters["gaze"]=="avoid":
            self.gaze(True)
        tts = self.session.service("ALTextToSpeech")
        speak_move_service = self.session.service("ALSpeakingMovement")
        tts.setLanguage("Italian") 
        tts.setVolume(self.volume[self.parameters["volume"]]) 
        if self.set_pitch==False:
            tts.setParameter("pitchShift",self.pitch[self.parameters["pitch"]])
            self.set_pitch==True
        tts.setParameter("speed",self.velocity[self.parameters["velocity"]])   
        anim_speech_service = self.session.service("ALAnimatedSpeech") 
        print("params voice set")
        for a in self.action_say:
            if a in self.action:
                thread = threading.Thread(target=self.task)
                # run the thread
                thread.start()
                # wait for the thread to finish
                self.execute(a,anim_speech_service)
                print('Waiting for the thread...')
                thread.join()
                
                break
        
        self.gaze(True)

    def speak(self,action,personality,params):
        if "l2" in action:
            actual_action=action.split(" ")
            self.location=actual_action.pop()          
        self.action=" ".join(actual_action)
        self.personality=personality
        self.parameters=params
        self.set_params()
        
        
