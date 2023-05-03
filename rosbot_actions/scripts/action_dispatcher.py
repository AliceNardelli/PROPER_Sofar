#!/usr/bin/env python
import os
import shutil
import subprocess
import json
import time
import numpy as np
from proper_lpg.srv import PersonalityGenerator, PersonalityGeneratorRequest
from proper_lpg.srv import ExecAction, ExecActionResponse
import rospy
from rosbot_actions.get_parameters import *
from rosbot_actions.class_speak import *
from rosbot_actions.class_navigation import *
from rosbot_actions.class_gesture import *



def dispatch_action(req):
    print(req)
    #ask parameters
    rospy.wait_for_service('personality_generator_srv')
    try:
        personality_generator_srv = rospy.ServiceProxy('personality_generator_srv', PersonalityGenerator)
        msg=PersonalityGeneratorRequest()
        msg.action=req.action
        msg.personality=req.personality
        resp = personality_generator_srv(msg)
        print(resp)       
        mmap =get_map(resp.params)
        print(mmap)
        s=Speak()
        n=Move()
        g=Gesture()
        if (mmap["speed"]=="no_active" or mmap["prox"]=="no_active") and (mmap["velocity"]!="no_active" and mmap["pitch"]!="no_active"):
                print(req.action,"action say")
                s.speak()
                
        if mmap["pitch"]=="no_active" and mmap["amplitude"]=="no_active" and mmap["head"]=="no_active":
                print(req.action,"action nav")
                n.move()

        if (mmap["speed"]=="no_active" or mmap["prox"]=="no_active") and (mmap["pitch"]=="no_active" or mmap["velocity"]=="no_active"):
                print(req.action,"action  gesture")
                g.gesture()
        
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
    #execute 
    return True

if __name__ == "__main__":
    rospy.init_node('action_dispatcher')
    s = rospy.Service('action_dispatcher_srv', ExecAction, dispatch_action)
    print("Ready to add two ints.")
    rospy.spin()




        
