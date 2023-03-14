#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use ALSpeakingMovement and ALAnimatedSpeech Modules"""

import qi
import argparse
import sys
import time

import random 

def stop_al(session):    
    al=session.service("ALAutonomousLife")
    al.setState("solitary")
    al.stopAll()    
    awr = session.service("ALBasicAwareness")
    print(al.getState())
    print(awr.isRunning(),awr.isEnabled())
    awr.setEnabled(False)
    awr.pauseAwareness()
    print(awr.isRunning(),awr.isEnabled())
    print("----------------")
    
def single_head_nod(session,motion_service, move):
    names  = ["HeadYaw", "HeadPitch"]
    if move=="nodding":
    	angles  = [0, 0.2]
    elif move=="shaking":
        print("one")
        angles =[0.6,0]
    else: #shaking down
        angles = [0.6, 0.2]
    fractionMaxSpeed  = 0.1
    motion_service.setAngles(names, angles, fractionMaxSpeed)
    time.sleep(2)
    if move=="nodding":
    	angles  = [0, 0.2]
    elif move=="shaking":
        angles =[-0.6,0]
        print("two")
    else:
        angles=[-0.6,0.2]
    motion_service.setAngles(names, angles, fractionMaxSpeed)
    time.sleep(2)
    
def nodding(session):
    stop_al(session)
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses("Head", 1.0)
    for i in range(10):
       single_head_nod(session, motion_service,"nodding")
       stop_al(session)
    motion_service.setStiffnesses("Head", 0.0)
       
       
def shaking(session,r):
    stop_al(session)
    motion_service = session.service("ALMotion")
    motion_service.setStiffnesses("Head", 1.0)   
    for i in range(r):
       single_head_nod(session,motion_service, "shaking")
    motion_service.setStiffnesses("Head", 1.0)
       
def single_move_head(session,motion_service,p,y,v):
    """
    This example uses the setAngles method.
    """
    stop_al(session)
    names  = ["HeadYaw", "HeadPitch"]
    angles  = [y, p]
    fractionMaxSpeed  = v
    motion_service.setAngles(names, angles, fractionMaxSpeed)
    
    time.sleep(2)
       
def non_agreeable(session):
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses("Head", 1.0)
    shaking(session,3)
    single_move_head(session,motion_service,0.3,0.6,0.1)
    single_move_head(session,motion_service,-0.3,-0.6,0.1)
    single_move_head(session,motion_service,-0.2,0.1,0.1)
    motion_service.setStiffnesses("Head", 0.0)
        
def non_conscientious(session):
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses("Head", 1.0)
    stop_al(session)
    for i in range(2):
       time.sleep(random.randint(0,3))
       single_head_nod(session,motion_service, "shaking down")
       stop_al(session)
    motion_service.setStiffnesses("Head", 0.0)
    
def conscientious(session):
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses("Head", 1.0)
    for i in range(10):
       single_move_head(session,motion_service, -0.1, round(random.uniform(-1, +1), 2), 0.1)
    motion_service.setStiffnesses("Head", 0.0)

def extrovert(session):
    """
    This example uses the setAngles method.
    """
    # Get the service ALMotion.

    motion_service  = session.service("ALMotion")
    for i in range(8):
	    motion_service.setStiffnesses("Head", 1.0)
	   
	    # Example showing how to set angles, using a fraction of max speed
	    r1 =round(random.uniform(-1, +1), 2)
	    r2 =round(random.uniform(-1, +1), 2)
	    names  = ["HeadYaw", "HeadPitch"]
	    angles  = [r1, r2]
	    fractionMaxSpeed  = 0.2
	    motion_service.setAngles(names, angles, fractionMaxSpeed)
	    time.sleep(random.randint(0,4))
    motion_service.setStiffnesses("Head", 0.0)



    

def main(session):
    """
    This example uses the goToPosture method.
    """
    # Get the service ALRobotPosture.

    awr = session.service("ALBasicAwareness")
    awr.setEnabled(True)
    time.sleep(5)



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
        
    
    #extrovert(session) #extro
    #time.sleep(3)
    #shaking(session,10)  #intro
    #nodding(session) #agree
    #non_agreeable(session) #non_agree
    #conscientious(session) #cosc
    non_conscientious(session) #non_cosc
   
