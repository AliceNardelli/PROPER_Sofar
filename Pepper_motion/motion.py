#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use ALSpeakingMovement and ALAnimatedSpeech Modules"""

import qi
import argparse
import sys
import time
from head_movement import *

def main(session):
    """
    This example uses the goToPosture method.
    """
    # Get the service ALRobotPosture.
    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 1.0)
    posture_service.goToPosture("SitRelax", 1.0)
    posture_service.goToPosture("StandZero", 1.0)
    posture_service.goToPosture("LyingBelly", 1.0)
    posture_service.goToPosture("LyingBack", 1.0)
    posture_service.goToPosture("Stand", 1.0)
    posture_service.goToPosture("Crouch", 1.0)
    posture_service.goToPosture("Sit", 1.0)

    print(posture_service.getPostureFamily())


def animation(session):
  animation_player_service = session.service("ALAnimationPlayer")
  animation_player_service.run("animations/Stand/Gestures/Me_1")
  animation_player_service.runTag("here")

def introversion(session):   
    tts = session.service("ALTextToSpeech")
    speak_move_service = session.service("ALSpeakingMovement")
    tts.setLanguage("Italian")
    #tts.setVolume(0.5) 
    #tts.setParameter("pitchShift",0)
    tts.setParameter("speed",90)    
    anim_speech_service = session.service("ALAnimatedSpeech")
    anim_speech_service.say("Ciao, ti pice la musica? A me piace molto la musica classica e spesso vado ad ascoltare dei concerti") 
    #anim_speech_service.say("No preferisco allenarmi da solo. Ho il mio orario, la mia tabella e le mie cuffiette")
    time.sleep(1)
    
    
def extroversion(session):   
    tts = session.service("ALTextToSpeech")
    speak_move_service = session.service("ALSpeakingMovement")
    tts.setLanguage("Italian") 
    #tts.setVolume(1) 
    #tts.setParameter("pitchShift",1)
    tts.setParameter("speed",110)   
    anim_speech_service = session.service("ALAnimatedSpeech") 
    anim_speech_service.say("Ciao, ti pice la musica? A me piace molto la musica classica e spesso vado ad ascoltare dei concerti")   
    #anim_speech_service.say("Non ti preoccupare, capisco che sei molto impegnato. Gli sport di squadra ti piacciono invece? Ad esempio beach volley, calcio, basket, io li adoro.")
    time.sleep(1)
    

def motion(session):
    m=session.service("ALMotion")
    
    #"ShoulderPitch","ShoulderRoll","ElbowYaw","ElbowRoll","WristYaw","Hand" L o R davanti
    #m.angleInterpolationWithSpeed(name,target angles (rad), max speed frac)
    
    frac_speed=1
    #angle=[-0.1 ,0.8,-2,-0.1,1.3]
    angle=[-0.1 ,0.8,-2,-0.1,0]
    angle=[-0.1 ,0.8,0,-0.6,-0]
   
    m.angleInterpolationWithSpeed(["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw"],angle,frac_speed) 
    m.openHand('LHand')
    time.sleep(6)
    
def say_head(session):
    tts = session.service("ALTextToSpeech")
    speak_move_service = session.service("ALSpeakingMovement")
    tts.setLanguage("Italian") 
    anim_speech_service = session.service("ALAnimatedSpeech") 
    big_shaking(session)
    anim_speech_service.say("Provo a muovere la testa contemporaneamente al parlato")
    

def navigation(session):
        #navigation_service = session.service("ALNavigation")
        #navigation_service.startFreeZoneUpdate()
        #navigation_service.setOrthogonalSecurityDistance(1)       
        mv=session.service("ALMotion")
        mv.setOrthogonalSecurityDistance(0.5)
        #mv.move(1,0,0)
        result = mv.getRobotVelocity()
        print("Robot Velocity: ", result)
        res=mv.moveTo(2,0,0,[["MaxVelXY",0.1]])
        print(res)
        #desiredRadius = 0.6
        #displacementConstraint = 0.5
        #result =nv.findFreeZone(desiredRadius, displacementConstraint)
       
def main(session):
        al= session.service("ALAutonomousLife")
        print(al.getState())
        time.sleep(1)
        tts = session.service("ALTextToSpeech")
        tts.setLanguage("Italian")
        tts2=session.service("ALMemory")
        tts4=session.service("ALSpeechRecognition")  
        #tts.say("s\xc3\xac") 
        tts4.setLanguage("Italian")
        tts4.setAudioExpression(True)
        #tts4.setVocabulary(["no", "sì", "si", "s\xc3\xac","bene","finito"],False)
        print("------------------")
        tts4.subscribe("WordRecognized")
        time.sleep(3)
        answ=tts2.getData("WordRecognized")
        print(answ)
        tts4.unsubscribe("WordRecognized")


def main2(session):
        al= session.service("ALAutonomousLife")
        al.setState("solitary")
        tts = session.service("ALTextToSpeech")
        tts.setLanguage("Italian")
        tts2=session.service("ALMemory")
        tts4=session.service("ALSpeechRecognition")
        tts4.setLanguage("Italian")
        #tts4.setVocabulary(["no", "sì", "si", "s\xc3\xac","bene"],True)
        tts4.setAudioExpression(True)
        print("------------------")
        tts4.subscribe("SpeechDetected")
        time.sleep(3)
        answ=tts2.getData("SpeechDetected")
        print(answ)
        tts4.unsubscribe("SpeechDetected")

def touch_detected(value): #esempio di callback
    print (value)

def main3(session):
        memory=session.service("ALMemory")
        touch = memory.subscriber("MiddleTactilTouched") #questo permette la callback
        connection = touch.signal.connect(touch_detected) #segnale della sottoscrizione
        time.sleep(10)
        #face_det=memory.getData("ALTouch")

def main4(session):
        #al=session.service("ALAutonomousLife")
        #al.setState("disabled")
        #m=session.service("ALMotion")
       # m.wakeUp()
        t=session.service("ALTracker")
        print(t.getAvailableModes())
        t.track("People")
        t.stopTracker()
        time.sleep(10)

   
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.135",
                        help="Robot IP address. On robot or Local Naoqi: use '130.251.13.132'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
        
    
    #main4(session)
    motion(session)

