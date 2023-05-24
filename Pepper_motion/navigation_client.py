#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use ALSpeakingMovement and ALAnimatedSpeech Modules"""

import qi
import argparse
import sys
import requests
from collections import OrderedDict
import numpy as np
from PIL import Image
import time

g_name=["r1","r2"]

goals={"r1":[1.2,0,0.0],
       "r2":[-1.2,0,3.14]}

goals_ids={
    "r1":13,
    "r2":24
}

goals_aruco_frame={
    "r1":[1.2,0,0],
    "r2":[1.2,0,0]
}

url='http://127.0.0.1:50010/'
headers= {'Content-Type':'application/json'}

pp=[0,0,0]

data = {
    "goal": 0,
}

def nav(session,x,y,yaw):
    mv=session.service("ALMotion")
    mv.setTangentialSecurityDistance(0.1)
    time.sleep(2)
    print("reaching "+str(x) +", "+str(y) +", "+str(yaw) +", ")
    res=mv.moveTo(x,y,yaw,[["MaxVelXY",0.3]])
    print(res)
    if res==False:
        res=mv.moveTo(x,y,yaw,[["MaxVelXY",0.3]])


def read_save_image(session,num):
    """
    First get an image, then show it on the screen with PIL.
    """
    # Get the service ALVideoDevice.
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

    im.save("/home/alice/images/"+str(num)+".png", "PNG")

    #im.show()

def start_motion(session, final_location):
   print("starting motion")
   global pp
   g=goals[final_location]
   start_command_x=abs(g[0]-pp[0])
   start_command_y=abs(g[1]-pp[1])
   start_command_yaw=abs(g[2]-pp[2])
   nav(session,start_command_x,start_command_y,start_command_yaw)
   #print(start_command_x,start_command_y,start_command_yaw) #send command
   read_save_image(session,goals_ids[final_location])
   data["goal"]=goals_ids[final_location]
   resp=requests.put(url+'commands', json=data, headers=headers)
   adjst=eval(resp.text)["success"]
   if adjst=="True":
        print("there")
        t=eval(resp.text)["translation"]
        tr=list(t.replace(",","").replace("[","").replace("]","").split(" "))
        xyz=[float(i) for i in tr]
        t=eval(resp.text)["rpy"]
        tr=list(t.replace(",","").replace("(","").replace(")","").split(" "))
        rpy=[float(i) for i in tr]
        command_x=goals_aruco_frame[final_location][0]-xyz[0]
        command_y=goals_aruco_frame[final_location][1]-xyz[1]
        command_yaw=goals_aruco_frame[final_location][2]-rpy[2]
        #nav(session,command_x,command_y,command_yaw)
        print("new navigation command")
        print(command_x,command_y,command_yaw)
   else:
       print("nothing to adjust")
   pp=goals[final_location] #update robot position


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.106",
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

    #al=session.service("ALAutonomousLife")
    #time.sleep(1)
    #al.setState("disabled")
    #m=session.service("ALMotion")
    #m.wakeUp()
    c=0
    for i in range(2):
        start_motion(session, g_name[c])
        c+=1
        if c==2:
            c=0