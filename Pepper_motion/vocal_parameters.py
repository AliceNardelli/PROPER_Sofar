#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use ALSpeakingMovement and ALAnimatedSpeech Modules"""

import qi
import argparse
import sys
import time

 
def agreeableness(session):   
    tts = session.service("ALTextToSpeech")
    speak_move_service = session.service("ALSpeakingMovement")
    tts.setLanguage("Italian") 
    tts.setVolume(0.75) 
    tts.setParameter("pitchShift",0.83)
    tts.setParameter("speed",90)   
    anim_speech_service = session.service("ALAnimatedSpeech") 
    anim_speech_service.say("Ciao, ti pice la musica?")   
    #anim_speech_service.say("Non ti preoccupare, capisco che sei molto impegnato. Gli sport di squadra ti piacciono invece? Ad esempio beach volley, calcio, basket, io li adoro.")
    time.sleep(1) 
  
def non_agreeableness(session):   
    tts = session.service("ALTextToSpeech")
    speak_move_service = session.service("ALSpeakingMovement")
    tts.setLanguage("Italian") 
    tts.setVolume(0.75) 
    tts.setParameter("pitchShift",0.95)
    tts.setParameter("speed",105)   
    anim_speech_service = session.service("ALAnimatedSpeech") 
    anim_speech_service.say("Ciao, ti pice la musica?")   
    #anim_speech_service.say("Non ti preoccupare, capisco che sei molto impegnato. Gli sport di squadra ti piacciono invece? Ad esempio beach volley, calcio, basket, io li adoro.")
    time.sleep(1) 
    
    
def coscientous(session):   
    tts = session.service("ALTextToSpeech")
    speak_move_service = session.service("ALSpeakingMovement")
    tts.setLanguage("Italian") 
    tts.setVolume(0.5) 
    tts.setParameter("pitchShift",0.95)
    tts.setParameter("speed",80)   
    anim_speech_service = session.service("ALAnimatedSpeech") 
    anim_speech_service.say("Ciao, ti pice la musica?")   
    #anim_speech_service.say("Non ti preoccupare, capisco che sei molto impegnato. Gli sport di squadra ti piacciono invece? Ad esempio beach volley, calcio, basket, io li adoro.")
    time.sleep(1) 
    
    
def non_coscientous(session):   
    tts = session.service("ALTextToSpeech")
    speak_move_service = session.service("ALSpeakingMovement")
    tts.setLanguage("Italian") 
    tts.setVolume(0.4) 
    tts.setParameter("pitchShift",0.83)
    tts.setParameter("speed",105)   
    anim_speech_service = session.service("ALAnimatedSpeech") 
    anim_speech_service.say("Ciao, ti pice la musica?")   
    #anim_speech_service.say("Non ti preoccupare, capisco che sei molto impegnato. Gli sport di squadra ti piacciono invece? Ad esempio beach volley, calcio, basket, io li adoro.")
    time.sleep(1) 
  

def introversion(session):   
    tts = session.service("ALTextToSpeech")
    speak_move_service = session.service("ALSpeakingMovement")
    tts.setLanguage("Italian")
    tts.setVolume(0.5) 
    tts.setParameter("pitchShift",0.95)
    tts.setParameter("speed",90)    
    anim_speech_service = session.service("ALAnimatedSpeech")
    anim_speech_service.say("Ciao, ti pice la musica?") 
    #anim_speech_service.say("No preferisco allenarmi da solo. Ho il mio orario, la mia tabella e le mie cuffiette")
    time.sleep(1)
    
    
def extroversion(session):   
    tts = session.service("ALTextToSpeech")
    speak_move_service = session.service("ALSpeakingMovement")
    tts.setLanguage("Italian") 
    tts.setVolume(1) 
    tts.setParameter("pitchShift",1.1)
    tts.setParameter("speed",110)   
    anim_speech_service = session.service("ALAnimatedSpeech") 
    anim_speech_service.say("Ciao, ti pice la musica?")   
    #anim_speech_service.say("Non ti preoccupare, capisco che sei molto impegnato. Gli sport di squadra ti piacciono invece? Ad esempio beach volley, calcio, basket, io li adoro.")
    time.sleep(1)
    
def baseline(session):
   
    tts = session.service("ALTextToSpeech")
    speak_move_service = session.service("ALSpeakingMovement")
    tts.setLanguage("Italian")
    
    anim_speech_service = session.service("ALAnimatedSpeech")

    anim_speech_service.say("Ciao, ti pice la musica?")
    time.sleep(1)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.104",
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
    #agreeableness(session)
    #non_agreeableness(session)
    #coscientous(session)
    #non_coscientous(session)
    
  

