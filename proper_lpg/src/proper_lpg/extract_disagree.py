#action1 avvicinarsi
#action2 esprimere gioia
#action3 consolare
#action4 fare pace
#bit 1 0:not touch 1 bouch
#bit 2,3 00:neutral 01:sad 10:angry 11:happydict={}
#agreeable personality
from proper_lpg.load_ontology import *
import random
import numpy as np

disagree_actions=["say_not_touch_me","say_to_move_far","say_something_about_angry","say_to_not_smile"]


zzz_d={"say_not_touch_me":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_move_far":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_about_angry":{"w1":4,"w2":2,"expected_outcome":[0,1,0]},
     "say_to_not_smile":{"w1":4,"w2":2,"expected_outcome":[0,1,0]},
     }

zzo_d={"say_not_touch_me":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
       "say_to_move_far":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_about_angry":{"w1":4,"w2":2,"expected_outcome":[0,1,0]},
     "say_to_not_smile":{"w1":2,"w2":1,"expected_outcome":[0,1,0]},
     }

zoz_d={"say_not_touch_me":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
       "say_to_move_far":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_about_angry":{"w1":2,"w2":1,"expected_outcome":[0,1,0]},
     "say_to_not_smile":{"w1":2,"w2":1,"expected_outcome":[0,1,0]},
     }

zoo_d={"say_not_touch_me":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
       "say_to_move_far":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_about_angry":{"w1":2,"w2":1,"expected_outcome":[0,1,0]},
     "say_to_not_smile":{"w1":4,"w2":2,"expected_outcome":[0,1,0]},
     }

ozz_d={"say_not_touch_me":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
       "say_to_move_far":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "say_something_about_angry":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_not_smile":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

ozo_d={"say_not_touch_me":{"w1":4,"w2":2,"expected_outcome":[0,1,0]},
      "say_to_move_far":{"w1":4,"w2":2,"expected_outcome":[0,1,0]}, 
     "say_something_about_angry":{"w1":4,"w2":2,"expected_outcome":[0,1,0]},
     "say_to_not_smile":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

ooz_d={"say_not_touch_me":{"w1":4,"w2":2,"expected_outcome":[0,0,1]},
       "say_to_move_far":{"w1":4,"w2":2,"expected_outcome":[0,0,1]},
     "say_something_about_angry":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,1]},
     "say_to_not_smile":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,1]},
     }

ooo_d={"say_not_touch_me":{"w1":4,"w2":2,"expected_outcome":[0,1,0]},
       "say_to_move_far":{"w1":4,"w2":2,"expected_outcome":[0,1,0]},
     "say_something_about_angry":{"w1":0,"w2":0,"expected_outcome":[0,1,0]},
     "say_to_not_smile":{"w1":4,"w2":2,"expected_outcome":[0,1,0]},
     }

disagreeableness_dict={
    "NT_N":{"weights":zzz_d,"num":[0,0,0]},
    "NT_S":{"weights":zzo_d,"num":[0,0,1]},
    "NT_A":{"weights":zoz_d,"num":[0,1,0]},
    "NT_H":{"weights":zoo_d,"num":[0,1,1]},
    "T_N":{"weights":ozz_d,"num":[1,0,0]},
    "T_S":{"weights":ozo_d,"num":[1,0,1]},
    "T_A":{"weights":ooz_d,"num":[1,1,0]},
    "T_H":{"weights":ooo_d,"num":[1,1,1]}
}



def choose_action_d(perception):
    global disagree_actions, disagreeableness_dict
    w=[]
    for a in disagree_actions:
        
        weight=disagreeableness_dict[perception]["weights"][a]["w1"]+disagreeableness_dict[perception]["weights"][a]["w2"]
        w.append(float(weight))
    norm = [i/sum(w) for i in w]
    to_execute=np.random.choice(disagree_actions,p=norm) #trovare il modo di normalizzare i pesi
    return to_execute, disagreeableness_dict[perception]["weights"][to_execute]["w1"]+disagreeableness_dict[perception]["weights"][to_execute]["w2"]



def update_weights_d(action, p_prev, p_after):
    list_real=disagreeableness_dict[p_after]["num"]
    list_expected=disagreeableness_dict[p_prev]["weights"][action]["expected_outcome"]
    error=0
    
    for i in range(0,len(list_real)):
        error+=(np.abs(list_real[i]-list_expected[i]))
    #normalize the error
    error=error/len(list_real)
    #update the weights
    prev=disagreeableness_dict[p_prev]["weights"][action]["w2"]
    
    if error==0:
        disagreeableness_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev+0.5),2)
        return round(np.abs(prev + 0.5),2)+disagreeableness_dict[p_prev]["weights"][action]["w1"]
    else:
        if prev<0.1:
            return  prev +disagreeableness_dict[p_prev]["weights"][action]["w1"]
        else:
           disagreeableness_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev - 0.5),2)
           return round(np.abs(prev - 0.5),2)+disagreeableness_dict[p_prev]["weights"][action]["w1"]