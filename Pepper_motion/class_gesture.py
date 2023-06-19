import time
import random
class Gesture:
    def __init__(self,session):
        self.session=session
        self.name="Pepper"
        self.action=""
        self.personality=""
        self.parameters={}
        self.disgust=["animations/Stand/Emotions/Negative/Angry_3",
                     "animations/Stand/Emotions/Negative/Bored_1",
                     "animations/Stand/Emotions/Negative/Disappointed_1",
                     "animations/Stand/Emotions/Negative/Frustrated_1",
                     "animations/Stand/Gestures/Angry_1",
                     "animations/Stand/Gestures/Angry_2",
                     "animations/Stand/Gestures/Desperate_1",
                     "animations/Stand/Gestures/Desperate_2",
                     "animations/Stand/Gestures/Desperate_3",
                     "animations/Stand/Gestures/Desperate_4",]
        
        self.excited=["animations/Stand/Emotions/Positive/Excited_1",
                      "animations/Stand/Emotions/Positive/Excited_3",
                      "animations/Stand/Emotions/Positive/Happy_4",
                      "animations/Stand/Emotions/Positive/Proud_2",
                      "animations/Stand/Gestures/Enthusiastic_3",
                      "animations/Stand/Gestures/Enthusiastic_4",
                      "animations/Stand/Gestures/Excited_1",]
        self.detached=["animations/Stand/Gestures/Thinking_2",
                       "animations/Stand/Gestures/Thinking_4",]
        
        self.hands=["animations/Stand/Joy_1",
                    "boston_animation_library/Stand/ta-da_01",
                    "boston_animation_library/Stand/ta-da_02",
                    "boston_animation_library/Stand/ta-da_03",
                    "boston_animation_library/Stand/ta-da_tacky",
                    ]
        
        self.rand_move=["Stand/Gestures/Confused_1",
                        "Stand/Gestures/Confused_2",
                        "Stand/Gestures/DontUnderstand_1",
                        "Stand/Gestures/IDontKnow_1",]
        
    def gesture(self, action,params):
        self.action=action
        self.parameters=params
        anim_speech_service = self.session.service("ALAnimatedSpeech") 
        animations={
            "show_disgust":self.disgust[random.randint(0,len(self.disgust)-1)],
            "show_excitement":self.excited[random.randint(0,len(self.excited)-1)],
            "show_hand":self.hands[random.randint(0,len(self.hands)-1)],
            "show_detachment":self.detached[random.randint(0,len(self.detached)-1)],
            "show_random_movement":self.rand_move[random.randint(0,len(self.rand_move)-1)],
        }
        app=animations[self.action]
        to_say="^start("+app+")\\pau=2000\\"
        print(to_say)
        anim_speech_service.say(to_say) 
        posture_service = self.session.service("ALRobotPosture")    
        posture_service.goToPosture("Stand", 0.1)
        


