#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
from PIL import Image
import argparse
import sys
import time
import requests
url='http://127.0.0.1:5009/'
headers= {'Content-Type':'application/json'}

data={
      "image":"",
}

def read_save_image(session):
    video_service = session.service("ALVideoDevice")
    print("Has depth camera",video_service.hasDepthCamera())
    resolution = 2    # VGA
    colorSpace = 11   # RGB     
    videoClient = video_service.subscribe("python_client", resolution, colorSpace, 5)
    naoImage = video_service.getImageRemote(videoClient)
    imageWidth = naoImage[0]
    imageHeight = naoImage[1]
    array = naoImage[6]
    image_string = str(bytearray(array))
    im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)
    im.save("/home/alice/images/image.png", "PNG")
    data["image"]="image.png"
    resp=requests.put(url+'face_detector', json=data, headers=headers)
    video_service.unsubscribe(videoClient)

    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.101",
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
    while True:
        time.sleep(1)
        read_save_image(session)