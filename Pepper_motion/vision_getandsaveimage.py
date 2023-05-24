#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Get an image. Display it and save it using PIL."""

import qi
import argparse
import sys
import time
from PIL import Image


def main(session):
    """
    First get an image, then show it on the screen with PIL.
    """
    # Get the service ALVideoDevice.
    video_service = session.service("ALVideoDevice")
    resolution = 2    # VGA
    colorSpace = 11   # RGB
    
    c=0
    while c<500:
        videoClient = video_service.subscribe("python_client", resolution, colorSpace, 5)
        naoImage = video_service.getImageRemote(videoClient)
        video_service.unsubscribe(videoClient)

        # Get the image size and pixel array.
        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        array = naoImage[6]
        image_string = str(bytearray(array))

        # Create a PIL Image from our pixel array.
        im = Image.frombytes("RGB", (imageWidth, imageHeight), image_string)

        # Save the image.
        im.save("/home/alice/images/pepper_c/image"+str(c)+".png", "PNG")
        c+=1
        time.sleep(0.5)


    #im.show()


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
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    #al=session.service("ALAutonomousLife")  
    #al.setState("disabled")
    #m=session.service("ALMotion")
    #m.wakeUp()
    p=session.service("ALRobotPosture")
    p.goToPosture("Stand",0.5)
    main(session)
