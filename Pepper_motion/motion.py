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
    angle=[-0.2 ,-0.8,0,0,1.3]
   
    m.angleInterpolationWithSpeed(["RShoulderPitch","RShoulderRoll","RElbowYaw","RElbowRoll","RWristYaw"],angle,frac_speed) 
    m.openHand('RHand')
    time.sleep(6)
    frac_speed=0.4
    angle=[0.0 ,-0.8,0,0.5,1.3]
    m.angleInterpolationWithSpeed(["RShoulderPitch","RShoulderRoll","RElbowYaw","RElbowRoll","RWristYaw"],angle,frac_speed)
    
    time.sleep(6)
    
    frac_speed=0.1
    angle=[0.1,-1,0,0.7,1.3]
    m.angleInterpolationWithSpeed(["RShoulderPitch","RShoulderRoll","RElbowYaw","RElbowRoll","RWristYaw"],angle,frac_speed)
    
    time.sleep(2)

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
    """
    This example uses the ALSpeechRecognition module.
    """
    # Get the service ALSpeechRecognition.

    asr_service = session.service("ALSpeechRecognition")

    asr_service.setLanguage("English")

    # Example: Adds "yes", "no" and "please" to the vocabulary (without wordspotting)
    vocabulary = ["yes", "no", "please"]
    asr_service.setVocabulary(vocabulary, False)

    # Start the speech recognition engine with user Test_ASR
    asr_service.subscribe("Test_ASR")
    print ('Speech recognition engine started')
    time.sleep(20)
    asr_service.unsubscribe("Test_ASR")


    


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
        
    
    #baseline(session) 
    #extroversion(session)
    #introversion(session)
    #animation(session)
    #main(session)
    #motion(session)
    #say_head(session)
    navigation(session)

