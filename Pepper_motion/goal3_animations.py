#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import time
import math
import random


def wake_up2(session):
    al=session.service("ALAutonomousLife")
    al.setState("disabled")
    m=session.service("ALMotion")
    m.wakeUp()
    posture_service = session.service("ALRobotPosture")
    posture_service.goToPosture("StandInit", 1.0)


def breath(session, anim_speech_service):
        for i in range(4):
            app="Stand/Waiting/Relaxation_2"
            to_say="^start("+app+")\\pau=6500\\"
            anim_speech_service.say(to_say)     
        posture_service = session.service("ALRobotPosture")    
        posture_service.goToPosture("Stand", 0.1)


def curl(session, anim_speech_service):
        app="Stand/Waiting/Fitness_1"
        to_say="^start("+app+")\\pau=13000\\"
        print(to_say)
        for i in range(3):
            anim_speech_service.say(to_say) 
        posture_service = session.service("ALRobotPosture")    
        posture_service.goToPosture("Stand", 0.1)

def blink(session, reps, secs, color):
    blink_service=session.service("ALLeds")
    name = 'FaceLeds'
    for i in range(reps):
        blink_service.fadeRGB(name,color,secs)   
        time.sleep(1) 
        blink_service.off(name)


def list_to_rad(pose):
    pose_rad=[]
    for p in pose:
         pose_rad.append(math.radians(p))
    return pose_rad



def yoga(session,velocity,reps):
    m=session.service("ALMotion")
    frac_speed=0.5
    joints=["RElbowRoll","RElbowYaw","RHand","RShoulderPitch","RShoulderRoll","RWristYaw","LElbowRoll","LElbowYaw","LHand","LShoulderPitch","LShoulderRoll","LWristYaw"]
    pose1=[0.8, 86.2, 0, 44.9, -33, 70.3, -10.6, -98.1, 0.75, 89.7, 41.5, -101.6]
    pose2=[75, 14.2, 0, 8.7, -23.5, 41.2, -62.9, -8.3, 0.75, 1.6, 10.4, 35.3]
    pose3=[20.7, 14.2, 0, -84.1, -32.6, 41.2, -20.8, -8.4, 0.75, -83.9, 32.9, 33.4]
    pose4=[83.9, -14.8, 0, -79.8, -30.2, 14.2, -84.2, 14.6, 0.98, -79.4, 30.3, -15.7]
    
    pose1=list_to_rad(pose1)
    pose2=list_to_rad(pose2)
    pose3=list_to_rad(pose3)
    pose4=list_to_rad(pose4)
    if velocity=="high":
        duration=20
    elif velocity=="low":
        duration=30
    else:
        duration=25
    #pose1
    for i in range(reps):
        print("reaching pose 1")
        t=0
        while t<duration:
            t+=1
            m.angleInterpolationWithSpeed(joints,pose1,frac_speed)

        #pose2
        print("reaching pose 2")
        t=0
        while t<duration:
            t+=1
            m.angleInterpolationWithSpeed(joints,pose2,frac_speed)

        #pose3
        print("reaching pose 3")
        t=0
        while t<duration:
            t+=1
            m.angleInterpolationWithSpeed(joints,pose3,frac_speed)

        #pose4
        print("reaching pose 4")
        t=0
        while t<30:
            t+=1
            m.angleInterpolationWithSpeed(joints,pose4,frac_speed)

    posture_service = session.service("ALRobotPosture")    
    posture_service.goToPosture("Stand", 0.1)

def move_head_away(session):
    print("avoiding gaze")
    m=session.service("ALMotion")
    frac_speed=0.5
    joints= ["HeadYaw", "HeadPitch"]
    num=random.randint(0,2)
    if num==0:
        pose=list_to_rad([0.6,80])
    elif num==2:
        pose=list_to_rad([0.6,-80])
    else:
        pose=list_to_rad([20, -5])
    t=0
    while t<20:
        t+=1
        m.angleInterpolationWithSpeed(joints,pose,frac_speed)


def embrace(session):
    m=session.service("ALMotion")
    frac_speed=0.5
    joints=["RElbowRoll","RElbowYaw","RHand","RShoulderPitch","RShoulderRoll","RWristYaw","LElbowRoll","LElbowYaw","LHand","LShoulderPitch","LShoulderRoll","LWristYaw"]
    pose1=[11.5, 66.1, 1, -3.3, -14.0, 18.1, -6.5, -66.1, 0.94, -2.8, 14.0, -15.6]
    pose1=list_to_rad(pose1)
    #pose1
    print("reaching pose 1")
    t=0
    while t<40:
        t+=1
        m.angleInterpolationWithSpeed(joints,pose1,frac_speed)
    
    posture_service = session.service("ALRobotPosture")    
    posture_service.goToPosture("Stand", 0.1)

    

def high_five(session):
    m=session.service("ALMotion")
    frac_speed=0.5
    joints=["LElbowRoll","LElbowYaw","LHand","LShoulderPitch","LShoulderRoll","LWristYaw"]
    pose1=[ -6.5, -66.1, 1, -2.8, 14.0, -15.6]
    pose1=list_to_rad(pose1)
    #pose1
    print("reaching pose 1")
    t=0
    while t<30:
        t+=1
        m.angleInterpolationWithSpeed(joints,pose1,frac_speed)    
    posture_service = session.service("ALRobotPosture")    
    posture_service.goToPosture("Stand", 0.1)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.182",
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

   
    