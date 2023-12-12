#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import time
touched=False

def tablet(session,im):
    DEF_IMG_APP = "tablet_images"
    TABLET_IMG_DEFAULT = im
    #TABLET_IMG_DEFAULT = "police_logo.png"
    sTablet = session.service("ALTabletService")
    image_dir = "http://%s/apps/%s/img/" % (sTablet.robotIp(), DEF_IMG_APP)
    tablet_image = image_dir + TABLET_IMG_DEFAULT
    sTablet.showImage(tablet_image)
    time.sleep(4)
    sTablet.hideImage()

def point_an_object(session, params):
    m=session.service("ALMotion")
    if params["g_speed"]=="low":
        frac_speed=0.1
    elif params["g_speed"]=="mid":
        frac_speed=0.4
    else:
        frac_speed=1
    if params["amplitude"]=="low":
        #angle=[-0.2 ,-0.8,0,0,1.3]
        angle=[-0.1 ,0.8,0,-0.6,-0]
    elif params=="mid":
        #angle=[0.0 ,-0.8,0,0.5,1.3]
        angle=[-0.1 ,0.8,-2,-0.3,0]
    else:
        #angle=[-0.2 ,-1,0,0,1.3]
        angle=[-0.1 ,0.8,-2,-0.1,0]
    m.angleInterpolationWithSpeed(["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw"],angle,frac_speed)
    m.openHand('LHand')
    time.sleep(2)



def ask_pick_sweet(session):
    give_take_object_touch(session,1,1,True)
    time.sleep(2)
    give_take_object_touch(session,0,1,False)
    throw_object(session)

def throw_object(session):
    print("Throw obj")
    m=session.service("ALMotion")
    frac_speed=0.5
    angle=[-0.1 ,0.5,-0.0,-0.0,-0.0,1]
    chain=["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"]
    stiff=len(chain)*[1]
    m.setStiffnesses(chain,stiff)
    t=0
    while t<3:
        m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
        t+=1
    stiff=len(chain)*[0]
    m.setStiffnesses(chain,stiff)

def give_take_object_touch(session, hand, stiffness, need_touch):
    global touched
    m=session.service("ALMotion")
    tts2=session.service("ALMemory")
    frac_speed=0.5
    angle0=[-0.1 ,0.5,-1.56,-0.0,-1.7,0]
    angle=[-0.1 ,0.5,-1.56,-0.0,-1.7,hand]
    chain=["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"]
    t=0
    stiff=len(chain)*[1]
    m.setStiffnesses(chain,stiff)
    m.angleInterpolationWithSpeed(chain,angle0,frac_speed)
    if need_touch:
        touched=False
        touch = tts2.subscriber("MiddleTactilTouched") #questo permette la callback
        connection = touch.signal.connect(touch_detected) #segnale della sottoscrizione
        while touched==False:
            m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
            time.sleep(1)
            print("Hand open")
            t+=1
        touched=False
    stiff=len(chain)*[stiffness]
    m.setStiffnesses(chain,stiff)

def touch_detected(value): #esempio di callback
    global touched
    touched=True
    print("touched")
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.119",
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
