class Move:
    def __init__(self,session):
        self.session=session
        self.name="Pepper"
        self.action=""
        self.initial_loc=""
        self.final_loc=""
        self.personality=""
        self.parameters={}
        self.action_navigation=["move"]
        

    def set_params(self):
        print("moving from ",self.initial_loc," to ",self.final_loc )

        print(self.parameters)
        mv=self.session.service("ALMotion")
        print("setting proxemity")
        if self.parameters["prox"]=="far":
            distance=0.7
            print("FAR")
        elif self.parameters["prox"]=="mid":
            distance=0.5
        elif self.parameters["prox"]=="near":
            distance=0.3
        else:
            print("proxemity not found")
            distance=0.9
        print(distance)
        
        print("setting speed")
        if self.parameters["speed"]=="high":
            vel=1
        elif self.parameters["speed"]=="mid":
            vel=0.4
        elif self.parameters["speed"]=="low":
            vel=0.2
        else:
            vel=0.4
            print("velocity not found")
        if self.final_loc=="l2":
            x=5
            theta=0
        elif self.final_loc=="l1":
            distance=0.1
            x=0
            theta=3.14
        print(x)
        mv.setOrthogonalSecurityDistance(distance)
        mv.setTangentialSecurityDistance(distance)
        res=mv.moveTo(x,0,theta,[["MaxVelXY",vel]])
        if res==-1:
            res=mv.moveTo(x,0,theta,[["MaxVelXY",vel]])
        
        if self.final_loc=="l1":
            print("l1 moving along")
            x=2
            res=mv.moveTo(x,0,0,[["MaxVelXY",vel]])
            if res==-1:
                res=mv.moveTo(x,0,0,[["MaxVelXY",vel]])
            res=mv.moveTo(0,0,theta,[["MaxVelXY",vel]])
            if res==-1:
                res=mv.moveTo(0,0,theta,[["MaxVelXY",vel]])

                
    def move(self,action,personality,params):
        self.action=action
        extract_locations=action.split(" ")
        self.final_loc=extract_locations.pop()
        self.initial_loc=extract_locations.pop()
        self.personality=personality
        self.parameters=params
        print(self.final_loc)
        self.set_params()
        