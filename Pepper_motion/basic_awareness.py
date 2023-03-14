#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use ALSpeakingMovement and ALAnimatedSpeech Modules"""

import qi
import argparse
import sys
import time

import random 

def close_hand(session):
    """
    This example uses the closeHand method.
    """
    # Get the service ALMotion.

    motion_service  = session.service("ALMotion")

    # Example showing how to close the right hand.
    handName  = 'RHand'
    motion_service.closeHand(handName)
    
    
    
def single_move_head(session):
    """
    This example uses the setAngles method.
    """
    # Get the service ALMotion.
    al=session.service("ALAutonomousLife")
    al.setState("solitary")
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses("Head", 1.0)
    names  = ["HeadYaw", "HeadPitch"]
    angles  = [0, 0.4]
    fractionMaxSpeed  = 0.1
    motion_service.setAngles(names, angles, fractionMaxSpeed)
    time.sleep(2.0)
    al.stopFocus()
    al.stopAll()
    #motion_service.setStiffnesses("Head", 0.0)

def move_head(session):
    """
    This example uses the setAngles method.
    """
    # Get the service ALMotion.

    motion_service  = session.service("ALMotion")
    for i in range(6):
	    motion_service.setStiffnesses("Head", 1.0)
	   
	    # Example showing how to set angles, using a fraction of max speed
	    r1 =round(random.uniform(-1, +1), 2)
	    r2 =round(random.uniform(-1, +1), 2)
	    names  = ["HeadYaw", "HeadPitch"]
	    angles  = [r1, r2]
	    fractionMaxSpeed  = 0.2
	    motion_service.setAngles(names, angles, fractionMaxSpeed)
	    time.sleep(2.0)
	    motion_service.setStiffnesses("Head", 0.0)


def posture(session):
    """
    This example uses the goToPosture method.
    """
    # Get the service ALRobotPosture.

    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 2.0)
    time.sleep(5)
    print("due")
    posture_service.goToPosture("LyingBelly", 1.0)
    time.sleep(5)
    print("tre")
    posture_service.goToPosture("StandInit", 2.0)
 
    

def main(session):
    """
    This example uses the goToPosture method.
    """
    # Get the service ALRobotPosture.

    awr = session.service("ALBasicAwareness")
    awr.setEnabled(True)
    time.sleep(5)
    
def motion(session):
    """
    This example uses the goToPosture method.
    """
    # Get the service ALRobotPosture.

    mo = session.service("ALMotion")
    mo.setBreathEnabled("Body",True)
    time.sleep(5)
   
def track(session):
    """
    This example uses the goToPosture method.
    """
    # Get the service ALRobotPosture.

    mo = session.service("ALFaceDetection")
    print(mo.isTrackingEnabled())
    time.sleep(5)  
    
def head_movement(session):
    mo = session.service("ALMotion")

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
        
    
    #main(session) 
    #motion(session)
    #track(session)
    #posture(session)
    single_move_head(session)
    #close_hand(session)

