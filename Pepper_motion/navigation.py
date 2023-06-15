#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use ALSpeakingMovement and ALAnimatedSpeech Modules"""

import qi
import argparse
import sys
import time
import almath
import random 




def find_free(session):
	nv=session.service("ALNavigation")
	desiredRadius = 0.6
	displacementConstraint = 0.5
	print(nv.findFreeZone(desiredRadius, displacementConstraint))



def move_along(session):
   nv=session.service("ALNavigation")
   nv.moveAlong(["Composed", ["Holonomic", ["Line", [0.0, -1.0]], 0.0, 5.0]]) #alongy
   nv.moveAlong(["Composed", ["Holonomic", ["Line", [-1.0, 0.0]], 0.0, 5.0]]) #alongx
      

def main(session):
    mv=session.service("ALMotion")
    res=mv.moveTo(0,0,3.14,[["MaxVelXY",0.3]])
    print(res)


def main2(session):
    """
    Walk: Small example to make Nao walk with gait customization.
    NAO is Keyser Soze.
    This example is only compatible with NAO.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    # TARGET VELOCITY
    X         = 1.0
    Y         = 0.0
    Theta     = 0.0
    Frequency = 1.0
    print(motion_service.getMoveConfig("Min"))
    print(motion_service.getMoveConfig("Max"))
    # Defined a limp walk{MaxVelXY, MaxVelTheta, MaxAccXY, MaxAccTheta, MaxJerkXY, MaxJerkTheta, TorsoWy}
    motion_service.move(X, Y, Theta,[["MaxVelXY", 1],["MaxVelTheta", 0.2]])
   

    time.sleep(4.0)

    

    # stop walk in the next double support
    motion_service.stopMove()

    # Go to rest position
    motion_service.rest()

def gesture(session):
        tts=session.service("ALTextToSpeech")
        sm=session.service("ALSpeakingMovement")
        anim_speech_service = session.service("ALAnimatedSpeech")
        app="Stand/Gestures/Desperate_4"
        #to_say="^start('"+app+"')"
        to_say='^start(animations/Stand/Gestures/Hey_3) Ciao come ti senti oggi io sto molto bene'
        print(to_say)
        anim_speech_service.say(to_say) 
        #time.sleep(7)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.140",
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
        
    gesture(session)
   
