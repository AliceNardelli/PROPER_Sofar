import random
import time
from loc_functions import *
from goal3_animations import *

class Move:
    def __init__(self,session):
        self.session=session
        self.name="Pepper"
        self.action=""
        self.parameters={}
        wake_up(session)
        laser=session.service("ALLaser")
        laser.laserOFF() # set the security distance to zero
        

    def executing_nav_action(self):
        print("Executing: ",self.action)
        if self.parameters["prox"]=="far":
            distance=1.2
            print("Proxemity FAR")
        elif self.parameters["prox"]=="mid":
            distance=1
            print("Proxemity MID")
        elif self.parameters["prox"]=="near":
            distance=0.8
            print("Proxemity NEAR")
        else:
            print("proxemity not found")
            distance=1
        
        if self.parameters["speed"]=="high":
            vel=1
            print("Velocity HIGH")
        elif self.parameters["speed"]=="mid":
            vel=0.4
            print("Velocity MID")
        elif self.parameters["speed"]=="low":
            vel=0.2
            print("Velocity LOW")
        else:
            vel=0.4
            print("velocity not found")

        
        coordinate={
            "go_not_crowded_area":[0.5,0.5,3.14,3],
            "turn_on_back":[0,0,3.14],
            "move_away":[-0.5,0,0],
            "go_closer":[0.5,0,0],
            "go_near_human":[1,0,0],
        }
        if self.action=="move_the_head_to_avoid_gaze":
            move_head_away(self.session)
        else:
            nav(self.session,coordinate[self.action][0],coordinate[self.action][1],coordinate[self.action][2],vel,distance)
            if self.action=="turn_on_back":
                nav(self.session,coordinate[self.action][0],coordinate[self.action][1],coordinate[self.action][2],vel,distance)
            

    def move(self,action,params):
        self.action=action.split(" ")[0]
        self.parameters=params
        self.executing_nav_action()
        