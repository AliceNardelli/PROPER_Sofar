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
    
    angle=[1.31,-0.05,0,1.74,-0.7,-0.045,-0.1,-1.7,1,1.16,0.39,0.05,0,0]
    chain=["RElbowRoll","RElbowYaw","RHand","RShoulderPitch","RShoulderRoll","RWristYaw","LElbowRoll","LElbowYaw","LHand","LShoulderPitch","LShoulderRoll","LWristYaw","HeadYaw","HeadPitch"]
    #angle=[-0.1 ,0.5,-1.56,-0.0,-1.7,1]
    #chain=["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"]
    m.setStiffnesses(chain, len(chain)*[0.0])         
    
    tts2=session.service("ALMemory")
    touch = tts2.subscriber("MiddleTactilTouched") #questo permette la callback
    connection = touch.signal.connect(touch_detected) #segnale della sottoscrizione
    while touched==False:
        m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
        print("Hand open")

    #m.openHand('RHand')
    #time.sleep(6)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.113",
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