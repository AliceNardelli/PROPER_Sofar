import random
from animations import *
str="Ciao, chiamami Pepper. Non che mi interessi particolarmente conoscere il tuo nome, ma per questioni di cortesia reciproca, potresti dirmelo?"


def add_gestures(to_say):
        #replace whit pauses
        print("-----------")
        to_say=to_say.replace("...",".")
        print(to_say)
        print("-----------")
        signs=[".",",","!","?"]
            #signs=["."]
            #for s in signs:
                #indeces=[pos for pos, char in enumerate(to_say) if char == s]
        for pos, char in enumerate(to_say):
                 if char in signs:
                        print("-----------")
                        print(to_say)
                        staff=speaking_motions_big[random.randrange(len(speaking_motions_big))]
                        
                        ind=to_say.index(char)
                        
                        to_say=to_say[:(ind)] + " ^start("+staff+") "+ char + to_say[ind+1:] 
                        print(to_say)
                        ind=to_say.index(char)
                        print(ind)
                        if char==",":
                                to_say=to_say[:(ind-1)]+" \\pau=400\\ "+to_say[(ind+1):]
                        else:
                                to_say=to_say[:(ind-1)]+" \\pau=800\\ "+to_say[(ind+1):]
                        print(to_say)          
                    
        staff=listening_motions_big[random.randrange(len(listening_motions_big))]
        to_say=to_say+" ^start("+staff+") \\pau=200\\"
       
        print(to_say)
        return to_say 

add_gestures(str)