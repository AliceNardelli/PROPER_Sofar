#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use ALSpeakingMovement and ALAnimatedSpeech Modules"""

import qi
import argparse
from class_navigation import Move
from class_speak import Speak
from class_gesture import Gesture
from client_prova import *
import sys 
initial_location="l1"
tower_location="l2"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.135",
                        help="Robot IP address. On robot or Local Naoqi: use '130.251.13.135'.")
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
        
    
    n=Move(session)
    s=Speak(session)
    g=Gesture(session)
    plan, cost =server_interface()   
    for p in plan:
        action=p.replace("\n","").replace("(","").replace(")","").replace("_"," ").replace('"','')
        print(action.split(" ")[0])
        param , mmap, personality =get_params(action.split(" ")[0])
        print(personality)
        print(mmap)
        if (mmap["speed"]=="no_active" or mmap["prox"]=="no_active") and (mmap["velocity"]!="no_active" and mmap["pitch"]!="no_active"):
                print(action,"action say")
                s.speak(action,personality,mmap)
                
        if mmap["pitch"]=="no_active" and mmap["amplitude"]=="no_active" and mmap["head"]=="no_active":
                print(action,"action nav")
                n.move(action,personality,mmap)

        if (mmap["speed"]=="no_active" or mmap["prox"]=="no_active") and (mmap["pitch"]=="no_active" or mmap["velocity"]=="no_active"):
                print(action,"action  gesture")
                g.gesture(action,personality,mmap)
        
    
