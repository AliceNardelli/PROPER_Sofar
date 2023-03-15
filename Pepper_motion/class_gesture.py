import time
class Gesture:
    def __init__(self,session):
        self.session=session
        self.name="Pepper"
        self.action=""
        self.personality=""
        self.parameters={}
        self.action_gesture=["show tower"]
        self.location=""

    def gesture(self, action,personality,params):
        if "l2" in action:
            actual_action=action.split(" ")
            self.location=actual_action.pop()          
        self.action=" ".join(actual_action)
        self.action=action
        self.personality=personality
        self.parameters=params
        srv=self.session.service("ALAnimationPlayer")
        srv.run("animations/[posture]/Gestures/Hey_1")
        m=self.session.service("ALMotion")
        time.sleep(2)
        #"ShoulderPitch","ShoulderRoll","ElbowYaw","ElbowRoll","WristYaw","Hand" L o R davanti
        #m.angleInterpolationWithSpeed(name,target angles (rad), max speed frac)
        #http://doc.aldebaran.com/2-4/family/pepper_technical/joints_pep.html
        if self.parameters["g_speed"]=="low":
            frac_speed=0.1
        elif self.parameters["g_speed"]=="mid":
            frac_speed=0.3
        else:
            frac_speed=0.6
        if self.parameters["amplitude"]=="low":
            angle=-0.1
        elif self.parameters["amplitude"]=="mid":
            angle=0.0
        else:
            angle=0.1
        m.angleInterpolationWithSpeed(["RShoulderPitch"],[angle],frac_speed)
        time.sleep(2)
        print(action)
