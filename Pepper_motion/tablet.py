#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use angleInterpolation Method"""

import qi
import argparse
import sys
import time
import almath
import threading

a=True 
def callback(x, y):
            print ( y)
            a=False

def main(session):
        tabletService = session.service("ALTabletService")
        tabletService.showInputDialog("text","Comando","ok","cancel")
        # Don't forget to disconnect the signal at the end
        signalID = 0

        # function called when the signal onTouchDown is triggered


        # attach the callback function to onJSEvent signal
        tabletService.showInputDialog("text","Comando","ok","cancel")
        while a:
            signalID = tabletService.onInputText.connect(callback)
        
    

def tablet(session):
        DEF_IMG_APP = "tablet_images"
        TABLET_IMG_DEFAULT = "/home/alice/cogne2.png"
        sTablet = session.service("ALTabletService")
        print(sTablet.robotIp())
        image_dir = "http://%s/apps/%s/img/" % (sTablet.robotIp(), DEF_IMG_APP)
        print(image_dir)
        tablet_image = image_dir + TABLET_IMG_DEFAULT
        sTablet.showImage(tablet_image)
        time.sleep(3)

def touch_detected(value): #esempio di callback
        print(value)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.140",
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

    tablet(session)
    