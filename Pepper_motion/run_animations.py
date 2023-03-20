#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use ALSpeakingMovement and ALAnimatedSpeech Modules"""

import qi
import argparse
import sys
import time

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

    print posture_service.getPostureFamily()


def animation(session):
  animation_player_service = session.service("ALAnimationPlayer")
  animation_player_service.run("animations/Stand/Gestures/You_1")
  #animation_player_service.runTag("here")
  
  
def baseline(session):   
    tts = session.service("ALTextToSpeech")
    speak_move_service = session.service("ALSpeakingMovement")
    tts.setLanguage("Italian")   
    speak_move_service.setMode("contextual")
    anim_speech_service = session.service("ALAnimatedSpeech")
    """
    configuration = {"bodyLanguageMode":"contextual"}
    ttw = { "hello" : ["Ciao"],
            "everything" : ["tutti"] }
    speak_move_service.addTagsToWords(ttw)
    """
    anim_speech_service.say("Ciao ^start(animations/Stand/Gestures/Hey_1), ti pice la musica? Tutto qui sembra essere pronto per un concerto") # 
    animation_player_service = session.service("ALAnimationPlayer")
    time.sleep(1)
    animation_player_service.run("animations/Stand/Waiting/ShowSky_1")
   


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
        

    animation(session)
    #main(session) 	
    #baseline(session)

