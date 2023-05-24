
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

url='http://127.0.0.1:50010/'
headers= {'Content-Type':'application/json'}

pp=[0,0,0]

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
    time.sleep(1)
    al.setState("disabled")
    m=session.service("ALMotion")
    m.wakeUp()
    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 1.0)

def nav(session,x,y,yaw):
    mv=session.service("ALMotion")
    distance=0.1
    mv.setOrthogonalSecurityDistance(distance)
    mv.setTangentialSecurityDistance(distance)
    print("reaching "+str(x) +", "+str(y) +", "+str(yaw) +", ")
    res=mv.moveTo(0,0,yaw,[["MaxVelXY",0.3]])
    res=mv.moveTo(x,y,0,[["MaxVelXY",0.3]])
    print(res)
    if res==False:
        res=mv.moveTo(0,0,yaw,[["MaxVelXY",0.3]])
        res=mv.moveTo(x,y,0,[["MaxVelXY",0.3]])
        print(res)

def read_save_image(session):
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
    im.save("/home/alice/images/image.png", "PNG")

def localize(session):
    global data
    global pp
    read_save_image(session)
    #read and pass data from odometry
    #pos=l.getRobotPosition()
    pos=pp
    
    data["x"]=pos[0]
    data["y"]=pos[1]
    data["yaw"]=pos[2]
    
    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 0.5)
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses("Head", 1.0)
    motion_service.setAngles(["HeadYaw", "HeadPitch"], [0,0], 0.5)
    time.sleep(1)
    resp=requests.put(url+'odom_offset', json=data, headers=headers)
    x_a_p=float(eval(resp.text)["x"])
    y_a_p=float(eval(resp.text)["y"])
    yaw_a_p=float(eval(resp.text)["yaw"])
    
    return x_a_p,y_a_p,yaw_a_p
    

def start_motion(session, final_location):
   global pp
   pos=pp
   #pos=l.getRobotPosition()
   #negative anti clockwise
   g=goals[final_location]
   start_command_x=abs(g[0]-pos[0])
   start_command_y=abs(g[1]-pos[1])
   start_command_yaw=abs(g[2]-pos[2])
   pp[0]=g[0]
   pp[1]=g[1]
   pp[2]=g[2]
   print("Starting motion")
   nav(session,0,0,start_command_yaw)
   x_a_p,y_a_p,yaw_a_p=localize(session)
   adj=goals_aruco_frame[final_location]
   print("Adjusting yaw")
   print(x_a_p,y_a_p,yaw_a_p)
   print(adj)
   adj_command_x=adj[0]-x_a_p
   adj_command_y=adj[1]-y_a_p
   adj_command_yaw=yaw_a_p-adj[2]
   nav(session,0,0,adj_command_yaw)
   nav(session,start_command_x,start_command_y,0)
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.102",
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

    #wake_up(session)
    m=session.service("ALMotion")
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
    
   

 
    












