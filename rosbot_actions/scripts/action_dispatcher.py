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
import requests

url='http://127.0.0.1:5008/'
headers= {'Content-Type':'application/json'}

data={
      "action":"",
      "params":""
}

def dispatch_action(req):
    print(req)
    #ask parameters
    rospy.wait_for_service('personality_generator_srv')
    try:
        personality_generator_srv = rospy.ServiceProxy('personality_generator_srv', PersonalityGenerator)
        msg=PersonalityGeneratorRequest()
        msg.action=req.action.split("_")[0]
        print("--------------")
        print(msg.action)
        print("--------------")
        msg.personality=req.personality
        resp = personality_generator_srv(msg)     
        mmap =get_map(resp.params)
        no_action=True
        for x, y in mmap.items():
          if y!="no_active":
               no_action=False
               break
        if no_action:
                print(req.action,"not to execute")        
        
        else:
            if (mmap["speed"]=="no_active" or mmap["prox"]=="no_active") and (mmap["velocity"]!="no_active" and mmap["pitch"]!="no_active"):
                    print(req.action,"action say")
                    data["action"]=req.action
                    data["personality"]=req.personality
                    data["params"]=mmap
                    resp=requests.put(url+'speak_server', json=data, headers=headers)
                    
            if mmap["pitch"]=="no_active" and mmap["amplitude"]=="no_active" and mmap["head"]=="no_active":
                    print(req.action,"action nav")
                    data["action"]=req.action
                    data["params"]=mmap
                    resp=requests.put(url+'navigation_server', json=data, headers=headers)

            if (mmap["speed"]=="no_active" or mmap["prox"]=="no_active") and (mmap["pitch"]=="no_active" or mmap["velocity"]=="no_active"):
                    print(req.action,"action  gesture")
                    data["action"]=req.action
                    data["params"]=mmap
                    resp=requests.put(url+'gesture_server', json=data, headers=headers)
        
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
    #execute 
    return True

if __name__ == "__main__":
    rospy.init_node('action_dispatcher')
    s = rospy.Service('action_dispatcher_srv', ExecAction, dispatch_action)
    print("Ready to add two ints.")
    rospy.spin()




        
