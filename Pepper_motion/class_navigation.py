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
        par={i:self.parameters[i] for i in self.parameters if self.parameters[i]!="no_active"}
        self.parameters=par
        print("moving from ",self.initial_loc," to ",self.final_loc )
        navigation_service = self.session.service("ALNavigation")
        navigation_service.startFreeZoneUpdate()
        navigation_service.setOrthogonalSecurityDistance(1)
        motion_service=self.session.service("ALMotion")
        if self.parameters["speed"]=="low":
            speed=0.5
        elif self.parameters["speed"]=="mid":
            speed=0.8
        else:
            speed =1
        motion_service.move(1.0, 0.0,speed)

    def move(self,action,personality,params):
        self.action=action
        extract_locations=action.split(" ")
        self.final_loc=extract_locations.pop()
        self.initial_loc=extract_locations.pop()
        self.personality=personality
        self.parameters=params
        self.set_params()
        