import time
import random
class Gesture:
    def __init__(self,session):
        self.session=session
        self.name="Pepper"
        self.action=""
        self.personality=""
        self.parameters={}
        self.disgust=["Stand/Emotions/Negative/Angry_3",
                     "Stand/Emotions/Negative/Bored_1",
                     "Stand/Emotions/Negative/Disappointed_1",
                     "Stand/Emotions/Negative/Frustrated_1",
                     "Stand/Gestures/Angry_1",
                     "Stand/Gestures/Angry_2",
                     "Stand/Gestures/Desperate_1",
                     "Stand/Gestures/Desperate_2",
                     "Stand/Gestures/Desperate_3",
                     "Stand/Gestures/Desperate_4",]
        
        self.excited=["Stand/Emotions/Positive/Excited_1",
                      "Stand/Emotions/Positive/Excited_3",
                      "Stand/Emotions/Positive/Happy_4",
                      "Stand/Emotions/Positive/Proud_2",
                      "Stand/Gestures/Enthusiastic_3",
                      "Stand/Gestures/Enthusiastic_4",
                      "Stand/Gestures/Excited_1",]
        self.detached=["Stand/Gestures/Thinking_2",
                       "Stand/Gestures/Thinking_4",]
        

        
    def gesture(self, action,params):
        self.action=action
        self.parameters=params
        anim_speech_service = self.session.service("ALAnimatedSpeech") 
        animations={
            "show_disgust":self.disgust[random.randrange(len(self.disgust))],
            "show_excitement":self.excited[random.randrange(len(self.excited))],
            "show_hand":self.excited[random.randrange(len(self.excited))],
            "show_detachment":self.detached[random.randrange(len(self.detached))],
            "show_random_movement":self.detached[random.randrange(len(self.detached))],
        }
        app=animations[self.action]
        to_say='^start('+app+')'
        print(to_say)
        anim_speech_service.say(to_say) 
        time.sleep(3)
        print("executing",app)


