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
        self.p=0
        self.ve=0
        self.vo=0
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
        al=self.session.service("ALAutonomousLife")
        if boolean:
            al.setState("interactive")
        else:
            al.setState("solitary") #solitary
            al.stopAll() #VEDERE SE VA RIATTIVATO
        ab=self.session.service("ALAutonomousBlinking")
        ab.setEnabled(boolean)
        abm=self.session.service("ALBackgroundMovement")
        abm.setEnabled(boolean)
        aba=self.session.service("ALBasicAwareness")
        aba.setEnabled(boolean)
        alm=self.session.service("ALSpeakingMovement")
        alm.setEnabled(True)
        asm=self.session.service("ALListeningMovement")
        asm.setEnabled(boolean2)
        awr = self.session.service("ALBasicAwareness")
        awr.setEnabled(boolean)

    def execute(self,a,anim_speech_service):
        if a=="say welcome":
            if self.personality=="Extrovert":
                anim_speech_service.say("Ciao, mi chiamo Pepper e sono molto contento di conoscerti")
            else:
                anim_speech_service.say("Buongiorno, io sono Pepper") 
        elif a=="speak about rules":
            if self.personality=="Extrovert":
                anim_speech_service.say("Ti ho chiamato per aiutarmi a costruire una torre altissima con quei cubetti sul tavolo.")
            else:
                anim_speech_service.say("Potresti aiutarmi a costruire una torre ordinando i cubetti sopra il tavolo.")
        elif a=="ask to order tower":
            anim_speech_service.say("sistema il cubetto rosso alla base")
            time.sleep(2)
            anim_speech_service.say("Metti il cubetto blue sopra quello rosso")
            time.sleep(2)
            anim_speech_service.say("Ora impila il cubetto verde")
            time.sleep(2)
            anim_speech_service.say("E per finire il cubetto giallo in cima alla torre")
            time.sleep(2)
            if self.personality=="Extrovert":
                 anim_speech_service.say("Ma che bella torre che abbiamo costruito, grazie mille per avermi aiutato")
            else:
                 anim_speech_service.say("Grazie molte per il tuo aiuto")
        elif a=="talk":
             if self.personality=="Extrovert":
                anim_speech_service.say("Sono molto felice che tu sia venuto qui a trovarmi oggi. Te come ti senti?")
                
             else:
                anim_speech_service.say("Grazie per essere venuto.")   
        elif a=="say goodbye":
            if self.personality=="Extrovert":
                anim_speech_service.say("Ora il mio lavoro e finito, spero di rivederti presto mi sono divertito moltissimo a giocare con te. Buona giornata")
                
            else:
                anim_speech_service.say("Ora abbiamo finito e devo andare, ti auguro una buona giornata")
               
        else:
           anim_speech_service.say("Non posso esegure azioni")
        

        
    def set_params(self):
        #par={i:self.parameters[i] for i in self.parameters if self.parameters[i]!="no_active"}
        
        print(self.parameters)
        if self.parameters["gaze"]=="avoid":
            self.gaze(False,False)
        else:
            self.gaze(True,False)
        tts = self.session.service("ALTextToSpeech")
        speak_move_service = self.session.service("ALSpeakingMovement")
        tts.setLanguage("Italian") 
        print(self.parameters)
        if self.set_pitch==False:
            self.vo=self.volume[self.parameters["volume"]]
            #self.p=self.pitch[self.parameters["pitch"]]
            self.ve=self.velocity[self.parameters["velocity"]]
            self.set_pitch=True
        tts.setVolume(self.vo) 
        tts.setParameter("pitchShift",self.p)
        tts.setParameter("speed",self.ve)  
        time.sleep(1) 
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
        if self.parameters["gaze"]=="mutual":
            self.gaze(True,True)
        else:
            self.gaze(False,False) 

    def speak(self,action,personality,params):
        if "l2" in action:
            actual_action=action.split(" ")
            self.location=actual_action.pop()          
        self.action=" ".join(actual_action)
        self.personality=personality
        self.parameters=params
        self.set_params()
        
        
