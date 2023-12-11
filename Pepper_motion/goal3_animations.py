#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import time


def breath(session, anim_speech_service):
        app="Stand/Waiting/Relaxation_2"
        to_say="^start("+app+")\\pau=2000\\"
        print(to_say)
        anim_speech_service.say(to_say) 
        posture_service = session.service("ALRobotPosture")    
        posture_service.goToPosture("Stand", 0.1)


def curl(session, anim_speech_service):
        app="Stand/Waiting/Fitness_1"
        to_say="^start("+app+")\\pau=2000\\"
        print(to_say)
        anim_speech_service.say(to_say) 
        posture_service = session.service("ALRobotPosture")    
        posture_service.goToPosture("Stand", 0.1)

def blink(session, reps, secs, color):
    blink_service=session.service("ALLeds")
    name = 'FaceLeds'
    for i in range(reps):
        blink_service.fadeRGB(name,color,secs)    
        blink_service.off(name)

def yoga(session):
    m=session.service("ALMotion")
    frac_speed=0.5
    joints=["RElbowRoll","RElbowYaw","RHand","RShoulderPitch","RShoulderRoll","RWristYaw","LElbowRoll","LElbowYaw","LHand","LShoulderPitch","LShoulderRoll","LWristYaw"]
    pose1=[0.8, 86.2, 0.67, 44.9, -33, 70.3, -10.6, -98.1, 0.75, 89.7, 41.5, -101.6]
    pose2=[75, 14.2, 0.67, 8.7, -23.5, 41.2, -62.9, -8.3, 0.75, 1.6, 10.4, 35.3]
    pose3=[20.7, 14.2, 0.67, -84.1, -32.6, 41.2, -20.8, -8.4, 0.75, -83.9, 32.9, 33.4]
    pose4=[83.9, -14.8, 0.94, -79.8, -30.2, 14.2, -84.2, 14.6, 0.98, -79.4, 30.3, -15.7]
    #pose1
    t=0
    while t<20:
        t+=1
        m.angleInterpolationWithSpeed(joints,pose1,frac_speed)

    #pose2
    t=0
    while t<20:
        t+=1
        m.angleInterpolationWithSpeed(joints,pose2,frac_speed)

    #pose3
    t=0
    while t<20:
        t+=1
        m.angleInterpolationWithSpeed(joints,pose3,frac_speed)

    #pose4
    t=0
    while t<20:
        t+=1
        m.angleInterpolationWithSpeed(joints,pose4,frac_speed)