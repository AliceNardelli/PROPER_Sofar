#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use angleInterpolation Method"""

import qi
import argparse
import sys
import time
import almath
import threading

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
    


#wake_up(session)
give_take_object(session)
grasp_object(session)
throw_object(session)
give_take_object(session)
nav(session)