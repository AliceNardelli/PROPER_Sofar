
#! /usr/bin/env python
# -*- encoding: UTF-8 -*-


import argparse
import sys
import requests
from collections import OrderedDict
import numpy as np
from PIL import Image
import time

url='http://127.0.0.1:50010/'
headers= {'Content-Type':'application/json'}


data={
    "x":0,
    "y":0,
    "z":0,
    "yaw":0,
    "roll":0,
    "pitch":0
}

def wake_up(session):
    al=session.service("ALAutonomousLife")
    time.sleep(1)
    al.setState("disabled")
    m=session.service("ALMotion")
    m.wakeUp()
    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 1.0)

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

def localize():
    global data
    data["x"]=0.1
    data["y"]=-0.1
    data["yaw"]=0.2
    print("Data from odometry")
    print(data)
    resp=requests.put(url+'odom_offset', json=data, headers=headers)
    off_x=float(eval(resp.text)["x"])
    off_y=float(eval(resp.text)["y"])
    off_yaw=float(eval(resp.text)["yaw"])
    data["x"]=data["x"]-off_x
    data["y"]=data["y"]-off_y
    data["yaw"]=data["yaw"]-off_yaw
    print(data)

if __name__ == "__main__":
        localize()

 
    












