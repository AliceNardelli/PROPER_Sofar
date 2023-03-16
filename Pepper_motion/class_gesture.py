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
    
    def gaze(self,boolean):
        al=self.session.service("ALAutonomousLife")
        if boolean:
            al.setState("interactive")
        else:
            al.setState("solitary") #solitary
            al.stopAll()
        ab=self.session.service("ALAutonomousBlinking")
        ab.setEnabled(boolean)
        abm=self.session.service("ALBackgroundMovement")
        abm.setEnabled(boolean)
        aba=self.session.service("ALBasicAwareness")
        aba.setEnabled(boolean)
        alm=self.session.service("ALSpeakingMovement")
        alm.setEnabled(boolean)
        asm=self.session.service("ALSpeakingMovement")
        asm.setEnabled(boolean)
        awr = self.session.service("ALBasicAwareness")
        awr.setEnabled(boolean)

    def gesture(self, action,personality,params):
        if "l2" in action:
            actual_action=action.split(" ")
            self.location=actual_action.pop()          
        self.action=" ".join(actual_action)
        self.action=action
        self.personality=personality
        self.parameters=params
        m=self.session.service("ALMotion")
        #"ShoulderPitch","ShoulderRoll","ElbowYaw","ElbowRoll","WristYaw","Hand" L o R davanti
        #m.angleInterpolationWithSpeed(name,target angles (rad), max speed frac)
        #http://doc.aldebaran.com/2-4/family/pepper_technical/joints_pep.html
        if self.parameters["g_speed"]=="low":
            frac_speed=0.1
        elif self.parameters["g_speed"]=="mid":
            frac_speed=0.4
        else:
            frac_speed=1
        if self.parameters["amplitude"]=="low":
            angle=[-0.2 ,-0.8,0,0,1.3]
        elif self.parameters["amplitude"]=="mid":
            angle=[0.0 ,-0.8,0,0.5,1.3]
        else:
            angle=[-0.2 ,-0.8,0,0,1.3]
        m.angleInterpolationWithSpeed(["RShoulderPitch","RShoulderRoll","RElbowYaw","RElbowRoll","RWristYaw"],angle,frac_speed)
        time.sleep(2)
        self.gaze(True)
        print(action)
