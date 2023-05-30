
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import requests
from collections import OrderedDict
import numpy as np
from PIL import Image
import time
import threading
url='http://127.0.0.1:50010/'
headers= {'Content-Type':'application/json'}

pp=[0,0,0]
center=[0,0,0]
data={
    "x":0,
    "y":0,
    "z":0,
    "yaw":0,
    "roll":0,
    "pitch":0
}

g_name=["r1","r2"]

goals={"r1":[1.2,0,0.0],
       "r2":[-1.2,0,3.14]}

goals_ids={
    "r1":13,
    "r2":24
}

goals_aruco_frame={
    "r1":[1.2,0,-3.14],
    "r2":[1.8,0,-3.14]
}

def wake_up(session):
    al=session.service("ALAutonomousLife")
    al.setState("disabled")
    m=session.service("ALMotion")
    m.wakeUp()
    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 1.0)


def nav(session,x,y,yaw,vel,prox):
    mv=session.service("ALMotion")
    mv.setOrthogonalSecurityDistance(0.05)#0.05
    mv.setTangentialSecurityDistance(0.05)
    print("reaching "+str(x) +", "+str(y) +", "+str(yaw) +", prox "+", "+str(prox) +", vel"+str(vel) )
    res=mv.moveTo(0,0,yaw,[["MaxVelXY",vel]])
    time.sleep(1)
    if res==False:
        res=mv.moveTo(0,0,yaw,[["MaxVelXY",vel]])
        time.sleep(1)
    mv.setOrthogonalSecurityDistance(0.05)#0.3
    mv.setTangentialSecurityDistance(0.05)
    res=mv.moveTo(x,y,0,[["MaxVelXY",vel]])
    time.sleep(1)
    if res==False:
        res=mv.moveTo(x,y,0,[["MaxVelXY",vel]])
        time.sleep(1)
    useSensorValues=True
    print("Robot position")
    print(mv.getRobotPosition(useSensorValues))


def read_save_image(session,i):
    video_service = session.service("ALVideoDevice")
    resolution = 2    # VGA
    colorSpace = 11   # RGB     
    videoClient = video_service.subscribe("python_client", resolution, colorSpace, 5)
    naoImage = video_service.getImageRemote(videoClient)
    video_service.unsubscribe(videoClient)
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]
    image_string = str(bytearray(array))
    im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)
    im.save("/home/alice/images/image"+str(i)+".png", "PNG")

def head_thread(motion_service,posture_service):
    #motion_service.setStiffnesses("Head", 1.0)
    t=0
    while t<20:
       posture_service.goToPosture("Stand", 0.1)
       motion_service.setAngles(["HeadYaw", "HeadPitch"], [0,0], 0.1)
       t+=1
    #motion_service.setStiffnesses("Head", 0)
    
def localize(session):
    global data
    global pp
    motion_service  = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    motion_service.setStiffnesses("Head", 1)        
    posture_service.goToPosture("Stand", 0.1)
    motion_service.setAngles(["HeadYaw", "HeadPitch"], [0,0], 0.1)
    for i in range(2):
        read_save_image(session,i)
    motion_service.setStiffnesses("Head", 0) 
    pos=pp
    data["x"]=pos[0]
    data["y"]=pos[1]
    data["yaw"]=pos[2]
    resp=requests.put(url+'odom_offset', json=data, headers=headers)
    success=eval(resp.text)["success"]
    x_a_p=float(eval(resp.text)["x"])
    y_a_p=float(eval(resp.text)["y"])
    yaw_a_p=float(eval(resp.text)["yaw"])
    id=int(eval(resp.text)["id"])
    return success,x_a_p,y_a_p,yaw_a_p,id
    

def start_motion(session, final_location, vel ,prox):
   #nav(session,0,0,3.14, vel ,prox)
   success,x_a_p,y_a_p,yaw_a_p,id=localize(session)
   print(success,x_a_p,y_a_p,yaw_a_p,id,goals_ids[final_location])
   while success=="False" or id!=goals_ids[final_location]:
       print("while")
       nav(session,0,0,3.14, vel ,prox)
       success,x_a_p,y_a_p,yaw_a_p,id=localize(session)
       print(success,x_a_p,y_a_p,yaw_a_p,id)
   nav(session,x_a_p-prox,y_a_p,0, vel ,prox)
   if yaw_a_p>0:
       cmd_yaw=3.14-yaw_a_p 
   else:
       cmd_yaw=-3.14-yaw_a_p 
   nav(session,0,0,cmd_yaw, vel ,prox) 
   success,x_a_p,y_a_p,yaw_a_p,id=localize(session)
   if x_a_p>1:
      nav(session,x_a_p-prox,y_a_p,0, vel ,prox)  
   pp[0]=x_a_p
   pp[1]=y_a_p
   pp[2]=3.14
   


    
   

 
    












