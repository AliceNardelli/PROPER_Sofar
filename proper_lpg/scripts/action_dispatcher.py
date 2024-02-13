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
from proper_lpg.get_parameters import *
import requests


def dispatch_action(req):
    global robot_block, human_block
    

    try:
        rospy.wait_for_service('personality_generator_srv')
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
            return True
        #MOVE ACTION
        else:
            print("EXEC "+ str(req.action))
            if "pick_place" in  str(req.action):
                req2=MoveArmRequest()
                if "replace" in  str(req.action):
                    
                    req2.block=human_block
                    req2.block_owner="human"
                    human_block+=1
                else:
                    
                    req2.block=robot_block
                    req2.block_owner="robot"
                    robot_block+=1

                req2.final_pose=req.move
                req2.amplitude=mmap["amplitude"]
                req2.speed=mmap["g_speed"]
                print(req2)
                rospy.wait_for_service('/kinova_move_srv')
                kinova_srv = rospy.ServiceProxy('/kinova_move_srv', MoveArm)
                resp = kinova_srv(req2) 
                return True
                 
        
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




        
