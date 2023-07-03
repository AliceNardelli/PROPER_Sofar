#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use ALSpeakingMovement and ALAnimatedSpeech Modules"""

import qi
import argparse
import sys
import time
from head_movement import *

touched=False

def touch_detected(value): #esempio di callback
    global touched
    touched=True
    print("touched")
    

def motion(session):
    m=session.service("ALMotion")
    
    #"ShoulderPitch","ShoulderRoll","ElbowYaw","ElbowRoll","WristYaw","Hand" L o R davanti
    #m.angleInterpolationWithSpeed(name,target angles (rad), max speed frac)
    
    frac_speed=1
    angle_big=[0.85,0.1,0.0,-1.14,-0.37,-0.29]
    angle_med=[1.4,0.1,0.0,-1.14,-1.36,-0.29]
    angle_small=[1.5,1.22,0.0,1.14,-0.46,-0.83]
    chain=["RElbowRoll","RElbowYaw","RHand","RShoulderPitch","RShoulderRoll","RWristYaw"]
    m.setStiffnesses(chain, len(chain)*[0.0])         
    
    tts2=session.service("ALMemory")
    touch = tts2.subscriber("MiddleTactilTouched") #questo permette la callback
    connection = touch.signal.connect(touch_detected) #segnale della sottoscrizione
    while touched==False:
        m.angleInterpolationWithSpeed(chain,angle_small,frac_speed) 
        m.openHand('RHand')
        print("Hand open")

    #m.openHand('RHand')
    #time.sleep(6)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.107",
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
        
    motion(session)