#action1 allontanarsi
#action2 distogliere lo sguardo
#action3 guardare in basso e girarsi
#action4 non reagire
#bit 1 0:not touch 1 bouch
#bit 2,3 00:neutral 01:sad 10:angry 11:happydict={}
#agreeable personality
from proper_reasoning.load_ontology import *
import random
import numpy as np

intro_actions=["get_away","avoid_gaze","turn_on_back","not_react"]


zzz_i={"get_away":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "avoid_gaze":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "turn_on_back":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "not_react":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     }

zzo_i={"get_away":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "avoid_gaze":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "turn_on_back":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "not_react":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

zoz_i={"get_away":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "avoid_gaze":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "turn_on_back":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "not_react":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

zoo_i={"get_away":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "avoid_gaze":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "turn_on_back":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     "not_react":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     }

ozz_i={"get_away":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "avoid_gaze":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "turn_on_back":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "not_react":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     }

ozo_i={"get_away":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "avoid_gaze":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "turn_on_back":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "not_react":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     }

ooz_i={"get_away":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "avoid_gaze":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     "turn_on_back":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "not_react":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

ooo_i={"get_away":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "avoid_gaze":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "turn_on_back":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "not_react":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

introversion_dict={
    "NT_N":{"weights":zzz_i,"num":[0,0,0]},
    "NT_S":{"weights":zzo_i,"num":[0,0,1]},
    "NT_A":{"weights":zoz_i,"num":[0,1,0]},
    "NT_H":{"weights":zoo_i,"num":[0,0,0]},
    "T_N":{"weights":ozz_i,"num":[1,0,0]},
    "T_S":{"weights":ozo_i,"num":[1,0,1]},
    "T_A":{"weights":ooz_i,"num":[1,1,0]},
    "T_H":{"weights":ooo_i,"num":[1,1,1]}
}



def choose_action_i(perception):
    global intro_actions, introversion_dict
    w=[]
    for a in intro_actions:

        weight=introversion_dict[perception]["weights"][a]["w1"]+introversion_dict[perception]["weights"][a]["w2"]
        w.append(float(weight))

   
    norm = [i/sum(w) for i in w]
    to_execute=np.random.choice(intro_actions,p=norm) #trovare il modo di normalizzare i pesi
    return to_execute, introversion_dict[perception]["weights"][to_execute]["w1"]+introversion_dict[perception]["weights"][to_execute]["w2"]



def update_weights_i(action, p_prev, p_after):
    list_real=introversion_dict[p_after]["num"]
    list_expected=introversion_dict[p_prev]["weights"][action]["expected_outcome"]
    error=0
    #accumulate the error between the perception and the expected one
    for i in range(0,len(list_real)):
        error+=(np.abs(list_real[i]-list_expected[i]))
    #normalize the error
    error=error/len(list_real)
    #update the weights
    prev=introversion_dict[p_prev]["weights"][action]["w2"]
   
    if error==0:
        introversion_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev + 0.5),2)
        return round(np.abs(prev + 0.5),2)+introversion_dict[p_prev]["weights"][action]["w1"]
    else:
        if prev<0.1:
           
            return  prev+introversion_dict[p_prev]["weights"][action]["w1"]
        else:
           introversion_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev - 0.5),2)
           
           return round(np.abs(prev - 0.5),2)+introversion_dict[p_prev]["weights"][action]["w1"]
        

        