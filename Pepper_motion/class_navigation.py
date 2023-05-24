import random
import time

class Move:
    def __init__(self):
        #self.session=session
        self.name="Pepper"
        self.action=""
        self.parameters={}
        self.pp=[0,0,0]
        

    def executing_nav_action(self):
        #mv=self.session.service("ALMotion")
        print(self.action,self.pp)
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

        #mv.setOrthogonalSecurityDistance(distance)
        #mv.setTangentialSecurityDistance(distance)
        #x y yaw move  return_back sleep turn_only incremental
        x_r=random.random()
        y_r=random.random()
        s_r=random.uniform(2,7)
        coordinate={
            "move_to_production_room":[1.2,0,0,1,0,0,0,0],
            "move_to_assembly_room":[-1.2,0,3.14,1,0,0,0,0],
            "go_not_crowded_area":[1,1,0,1,1,1,0,1],
            "turn_on_back":[0,0,3.14,1,1,2,1,0],
            "go_far":[-1,0,0,1,0,0,0,1],
            "move_to_check_human_working_station":[0.2,0,0,1,0,0,0,1],
            "go_in_a_random_position":[x_r,y_r,3.14,1,1,s_r,0,1],
            "late":[0,0,0,0,0,s_r,0,0]
        }
        if coordinate[self.action][3]==1:
            if coordinate[self.action][6]==0:
                if coordinate[self.action][7]==0:
                    x=abs(coordinate[self.action][0] - self.pp[0])
                    y=abs(coordinate[self.action][1] - self.pp[1])
                    yaw=abs(coordinate[self.action][2] - self.pp[2])
                    print("going",x,y,yaw)
                else:
                    x=coordinate[self.action][0]
                    y=coordinate[self.action][1]
                    yaw=coordinate[self.action][2]
                    print("going",x,y,yaw)
            else:
                x=0
                y=0
                yaw=abs(coordinate[self.action][2])
                print("going",x,y,yaw)
            #res=mv.moveTo(0,0,yaw,[["MaxVelXY",vel]])
            #res=mv.moveTo(x,y,0,[["MaxVelXY",vel]])
        time.sleep(coordinate[self.action][5])
        print("sleeping",coordinate[self.action][5])
        if coordinate[self.action][4]==1:
            if coordinate[self.action][6]==0:
                if coordinate[self.action][7]==0:
                    x=abs(coordinate[self.action][0] - self.pp[0])
                    y=abs(coordinate[self.action][1] - self.pp[1])
                    yaw=abs(coordinate[self.action][2] - self.pp[2])+3.14
                    print("returning",x,y,yaw)
                else:
                    x=coordinate[self.action][0]
                    y=coordinate[self.action][1]
                    yaw=coordinate[self.action][2]+3.14
                    print("going",x,y,yaw)
            else:
                x=0
                y=0
                yaw=-abs(coordinate[self.action][2])
                print("returning",x,y,yaw)
            #res=mv.moveTo(0,0,yaw,[["MaxVelXY",vel]])
            #res=mv.moveTo(x,y,0,[["MaxVelXY",vel]])
            
        else:
            if coordinate[self.action][7]==0:
                self.pp[0]=coordinate[self.action][0]
                self.pp[1]=coordinate[self.action][1]
                self.pp[2]=coordinate[self.action][2]

            else:
                if self.pp[0]>0:
                   self.pp[0]=coordinate[self.action][0]+self.pp[0]
                else:
                    self.pp[0]=-coordinate[self.action][0]+self.pp[0]

                if self.pp[1]>0:
                   self.pp[1]=coordinate[self.action][1]+self.pp[1]
                else:
                    self.pp[1]=-coordinate[self.action][1]+self.pp[1]


                self.pp[2]=-coordinate[self.action][2]+self.pp[2]
                
        print(self.pp)   


    def move(self,action,params):
        self.action=action.split(" ")[0]
        self.parameters=params
        self.executing_nav_action()
        