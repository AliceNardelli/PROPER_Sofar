import time
class Gesture:
    def __init__(self):
        #self.session=session
        self.name="Pepper"
        self.action=""
        self.personality=""
        self.parameters={}
        
    def gesture(self, action,params):
        self.action=action
        self.parameters=params
        #animation_player_service = session.service("ALAnimationPlayer")
        
        animations={
            "show_disgust":"showing disgust",
            "show_excitement":"excited",
            "show_hand":"show hand",
            "show_detachment":"show detached",
            "show_random_movement":"showing dandom move"
        }
        app=animations[self.action]
        #animation_player_service.run(app)
        print("executing",app)


