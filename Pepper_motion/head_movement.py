#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
import qi
import argparse
import sys
import time
import random 

def stop_al(session):    
    al=session.service("ALAutonomousLife")
    al.setState("solitary")
    al.stopAll()    
    awr = session.service("ALBasicAwareness")
    print(al.getState())
    print(awr.isRunning(),awr.isEnabled())
    awr.setEnabled(False)
    awr.pauseAwareness()
    print(awr.isRunning(),awr.isEnabled())
    print("----------------")
    
def single_head_nod(session,motion_service, move):
    names  = ["HeadYaw", "HeadPitch"]
    if move=="nodding":
        angles  = [0, 0.2]
    elif move=="shaking":
        print("one")
        angles =[0.4,0]
    else: #shaking down
        angles = [0.4, 0.2]
    fractionMaxSpeed  = 0.1
    motion_service.setAngles(names, angles, fractionMaxSpeed)
    time.sleep(2)
    if move=="nodding":
        angles  = [0, 0.2]
    elif move=="shaking":
        angles =[-0.4,0]
        print("two")
    else:
        angles=[-0.4,0.2]
    motion_service.setAngles(names, angles, fractionMaxSpeed)
    time.sleep(1)
    
def nodding(session):
    #stop_al(session)
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses("Head", 1.0)
    for i in range(2):
       single_head_nod(session, motion_service,"nodding")
       #stop_al(session)
    motion_service.setStiffnesses("Head", 0.0)
       
       
def shaking(session,r):
    #stop_al(session)
    motion_service = session.service("ALMotion")
    motion_service.setStiffnesses("Head", 1.0)   
    for i in range(r):
       single_head_nod(session,motion_service, "shaking")
    motion_service.setStiffnesses("Head", 1.0)
       
def single_move_head(session,motion_service,p,y,v):
    """
    This example uses the setAngles method.
    """
    #stop_al(session)
    names  = ["HeadYaw", "HeadPitch"]
    angles  = [y, p]
    fractionMaxSpeed  = v
    motion_service.setAngles(names, angles, fractionMaxSpeed)
    time.sleep(1)
       
def shaking_low(session):
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses("Head", 1.0)
    shaking(session,2)
    single_move_head(session,motion_service,0.3,0.6,0.1)
    single_move_head(session,motion_service,-0.3,-0.6,0.1)
    single_move_head(session,motion_service,-0.2,0.1,0.1)
    motion_service.setStiffnesses("Head", 0.0)
        
def tilt_down_shaking(session):
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses("Head", 1.0)
    #stop_al(session)
    for i in range(2):
       time.sleep(random.randint(0,3))
       single_head_nod(session,motion_service, "shaking down")
       #stop_al(session)
    motion_service.setStiffnesses("Head", 0.0)
    
def tilt_up_shaking(session):
    motion_service  = session.service("ALMotion")
    motion_service.setStiffnesses("Head", 1.0)
    for i in range(3):
       single_move_head(session,motion_service, -0.1, round(random.uniform(-0.5, +0.5), 2), 0.1)
    motion_service.setStiffnesses("Head", 0.0)

def big_shaking(session):
    motion_service  = session.service("ALMotion")
    for i in range(4):
        motion_service.setStiffnesses("Head", 1.0)
        r1 =round(random.uniform(-0.5, +0.5), 2)
        r2 =round(random.uniform(-0.5, +0.5), 2)
        names  = ["HeadYaw", "HeadPitch"]
        angles  = [r1, r2]
        fractionMaxSpeed  = 0.2
        motion_service.setAngles(names, angles, fractionMaxSpeed)
        time.sleep(random.randint(0,1))
    motion_service.setStiffnesses("Head", 0.0)


   
