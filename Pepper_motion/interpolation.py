#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use angleInterpolation Method"""

import qi
import argparse
import sys
import time
import almath
import threading
from loc_functions import*
def wake_up(session):
        al=session.service("ALAutonomousLife")
        al.setState("disabled")
        m=session.service("ALMotion")
        m.wakeUp()
    

def grasp_object(session):
    m=session.service("ALMotion")
    frac_speed=0.5
    chain=["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"]
    t=0
    angle=[-0.1 ,0.5,-1.56,-0.0,-1.7,0]
    stiff=len(chain)*[1]
    m.setStiffnesses(chain,stiff)
    while t<5:
       m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
       time.sleep(1)
       t+=1
    t=0
    while t<5:
       m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
       time.sleep(1)
       t+=1
    stiff=len(chain)*[0]
    m.setStiffnesses(chain,stiff)
    

def give_take_object(session):
    m=session.service("ALMotion")
    frac_speed=0.5
    angle=[-0.1 ,0.5,-1.56,-0.0,-1.7,1]
    chain=["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"]
    t=0
    stiff=len(chain)*[1]
    m.setStiffnesses(chain,stiff)
    while t<5:
       m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
       time.sleep(1)
       t+=1
    stiff=len(chain)*[0]
    m.setStiffnesses(chain,stiff)


def give_take_object2(session):
    m=session.service("ALMotion")
    frac_speed=0.5
    angle=[-0.1 ,0.5,-1.56,-0.0,-1.7,0]
    chain=["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"]
    t=0
    stiff=len(chain)*[1]
    m.setStiffnesses(chain,stiff)
    while t<5:
       m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
       time.sleep(1)
       t+=1
    stiff=len(chain)*[0]
    m.setStiffnesses(chain,stiff)

def throw_object(session):
    m=session.service("ALMotion")
    frac_speed=0.5
    angle=[-0.1 ,0.5,-0.0,-0.0,-0.0,1]
    chain=["LShoulderPitch","LShoulderRoll","LElbowYaw","LElbowRoll","LWristYaw","LHand"]
    stiff=len(chain)*[1]
    m.setStiffnesses(chain,stiff)
    t=0
    while t<5:
       m.angleInterpolationWithSpeed(chain,angle,frac_speed) 
       t+=1
    stiff=len(chain)*[0]
    m.setStiffnesses(chain,stiff)
    
if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument("--ip", type=str, default="130.251.13.142",
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
   give_take_object(session)
   grasp_object(session)
   nav(session,1,0,3.14,1,0)
   give_take_object2(session)
   throw_object(session)
   