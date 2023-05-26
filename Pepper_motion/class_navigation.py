import random
import time
from loc_functions import *

class Move:
    def __init__(self,session):
        self.session=session
        self.name="Pepper"
        self.action=""
        self.parameters={}
        self.pp=[0,0,0]
        motion_service  = session.service("ALMotion")

        # Example that finds the difference between the command and sensed angles.
        names         = "Body"
        useSensors    = False
        commandAngles = motion_service.getAngles(names, useSensors)
        print(commandAngles)
        self.prox=0

    def executing_nav_action(self):
        print("Executing: ",self.action)
        if self.parameters["prox"]=="far":
            distance=0.7
            print("Proxemity FAR")
        elif self.parameters["prox"]=="mid":
            distance=0.5
            print("Proxemity MID")
        elif self.parameters["prox"]=="near":
            distance=0.3
            print("Proxemity NEAR")
        else:
            print("proxemity not found")
            distance=0.9
        
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
        if self.prox==0:
            self.prox=0.3
        
        #x y yaw move  return_back sleep turn_only incremental
        x_r=random.random()
        y_r=random.random()
        s_r=random.uniform(2,7)
        coordinate={
            "move_to_production_room":"r1",
            "move_to_assembly_room":"r2",
            "go_not_crowded_area":[0.5,0.5,3.14,3],
            "turn_on_back":[0,0,3.14,4],
            "go_far":[-0.5,0,0,2],
            "move_to_check_human_working_station":[0.2,0,0,3],
            "go_in_a_random_position":[x_r,y_r,3.14,s_r],
            "late":[0,0,0,s_r]
        }

        if coordinate[self.action]=="r1":
            start_motion(self.session, "r1",vel,self.prox)
        elif coordinate[self.action]=="r2":
            start_motion(self.session, "r2",vel,self.prox)           
        else:
            nav(self.session,coordinate[self.action][0],coordinate[self.action][1],coordinate[self.action][2])
            time.sleep(coordinate[self.action][3])
            print("sleeping",coordinate[self.action][3])
            nav(self.session, coordinate[self.action][0],coordinate[self.action][1],coordinate[self.action][2])


    def move(self,action,params):
        self.action=action.split(" ")[0]
        self.parameters=params
        self.executing_nav_action()
        