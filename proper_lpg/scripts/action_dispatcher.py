#!/usr/bin/env python
import os
import shutil
import subprocess
import json
import time
import numpy as np
from proper_lpg.srv import PersonalityGenerator, PersonalityGeneratorRequest
from proper_lpg.srv import ExecAction, ExecActionResponse
from pp_task.srv import MoveArm, MoveArmRequest
import rospy
from rosbot_actions.get_parameters import *
import requests


def dispatch_action(req):
    global robot_block, human_block
    rospy.wait_for_service('personality_generator_srv')

    try:
        personality_generator_srv = rospy.ServiceProxy('personality_generator_srv', PersonalityGenerator)
        msg=PersonalityGeneratorRequest()
        msg.action=req.action.split("_")[0]
        msg.personality=req.personality
        resp = personality_generator_srv(msg)     
        mmap =get_map(resp.params)
        #SPEAK ACTION
        if mmap["language"]!="no_active":
            if "say_human" in  str(req.action):
                human_block+=1
            input("press input to exec the action "+ str(req.action))
        #MOVE ACTION
        else:
            print("EXEC "+ str(req.action))
            if "pick_place" in  str(req.action):
                req2=MoveArmRequest()
                if "replace" in  str(req.action):
                    human_block+=1
                    req2.block=human_block
                    req2.block_owner="human"
                else:
                    robot_block+=1
                    req2.block=robot_block
                    req2.block="robot"

                req2.final_pose=msg.move
                req2.amplitude=mmap["amplitude"]
                req2.speed=mmap["g_speed"]
                kinova_srv = rospy.ServiceProxy('kinova_motion_srv', MoveArm)
                resp = kinova_srv(req2) 
                
                
                


            
        
        
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
    #execute 
    return True

if __name__ == "__main__":
    global robot_block, human_block
    robot_block=0
    human_block=0
    rospy.init_node('action_dispatcher')
    s = rospy.Service('action_dispatcher_srv', ExecAction, dispatch_action)
    print("Ready to add two ints.")
    rospy.spin()




        
