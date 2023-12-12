import time
import random
from goal2_animations import *
from goal3_animations import *

class Gesture:
    def __init__(self,session):
        self.session=session
        self.name="Pepper"
        self.action=""
        self.personality=""
        self.parameters={}
       
        
    def gesture(self, action,params):
        self.action=action.split(" ")[0]
        self.parameters=params
       
        posture_service = self.session.service("ALRobotPosture")    
        posture_service.goToPosture("Stand", 0.1)

        if self.action=="point_the_glass":
            point_an_object(self.session, self.parameters)

        


