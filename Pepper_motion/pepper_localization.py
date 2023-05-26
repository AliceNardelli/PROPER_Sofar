
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


def nav(session,x,y,yaw):
    mv=session.service("ALMotion")
    prox=0.3
    mv.setOrthogonalSecurityDistance(prox)
    mv.setTangentialSecurityDistance(prox)
    time.sleep(0.5)
    print("reaching "+str(x) +", "+str(y) +", "+str(yaw) +", ")
    res=mv.moveTo(0,0,yaw,[["MaxVelXY",0.3]])
    print(res)
    if res==False:
        res=mv.moveTo(0,0,yaw,[["MaxVelXY",0.3]])
    res=mv.moveTo(x,y,0,[["MaxVelXY",0.3]])
    print(res)
    if res==False:
        res=mv.moveTo(x,y,0,[["MaxVelXY",0.3]])


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
    for i in range(3):
        posture_service.goToPosture("Stand", 0.1)
        motion_service.setAngles(["HeadYaw", "HeadPitch"], [0,0], 0.1)
        read_save_image(session,i)
    #read and pass data from odometry
    #pos=l.getRobotPosition()
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
    

def start_motion(session, final_location):
   global pp, center
   #go to the center
   #nav(session,center[0]-pp[0],center[1]-pp[1],center[2]-pp[2])
   success,x_a_p,y_a_p,yaw_a_p,id=localize(session)
   print(success,x_a_p,y_a_p,yaw_a_p,id,goals_ids[final_location])
   print(id!=goals_ids[final_location])
   while success=="False" or id!=goals_ids[final_location]:
       print("while")
       nav(session,0,0,3.14)
       success,x_a_p,y_a_p,yaw_a_p,id=localize(session)
       print(success,x_a_p,y_a_p,yaw_a_p,id)
       time.sleep(0.5)
   nav(session,x_a_p,y_a_p,0)
   pp[0]=x_a_p
   pp[1]=y_a_p
   pp[2]=3.14
   
       
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.136",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))        
        #app = qi.Application(["TabletModule", "--qi-url=" + "tcp://" + args.ip + ":" + str(args.port)])
        #app.start()
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    wake_up(session)
    #m=session.service("ALMotion")
    #l=session.service("ALLocalization")
    #ret = l.learnHome()
   
    # Check that no problem occurred.
    #if ret == 0:
           # print("Learning OK")
    #else:
           # print ("Error during learning " + str(ret))

    c=0
    for i in range(6):
        print(g_name[c])
        start_motion(session, g_name[c])
        c+=1
        if c==2:
            c=0
    
   

 
    












