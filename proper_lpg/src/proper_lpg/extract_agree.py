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

agree_actions=["get_closer","express_happyness","express_empathy","make_peace"]


zzz_a={"get_closer":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     "express_happyness":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     "express_empathy":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "make_peace":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     }

zzo_a={"get_closer":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "express_happyness":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "express_empathy":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     "make_peace":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     }

zoz_a={"get_closer":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "express_happyness":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "express_empathy":{"w1":0.0,"w2":0.0,"expected_outcome":[0,1,1]},
     "make_peace":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     }

zoo_a={"get_closer":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "express_happyness":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     "express_empathy":{"w1":0.0,"w2":0.0,"expected_outcome":[0,1,1]},
     "make_peace":{"w1":0.0,"w2":0.0,"expected_outcome":[0,1,1]},
     }

ozz_a={"get_closer":{"w1":4,"w2":2,"expected_outcome":[1,1,1]},
     "express_happyness":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "express_empathy":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "make_peace":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     }

ozo_a={"get_closer":{"w1":2,"w2":1,"expected_outcome":[1,1,1]},
     "express_happyness":{"w1":0.0,"w2":0.0,"expected_outcome":[0,1,1]},
     "express_empathy":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     "make_peace":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     }

ooz_a={"get_closer":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "express_happyness":{"w1":0.0,"w2":0.0,"expected_outcome":[0,1,1]},
     "express_empathy":{"w1":0.0,"w2":0.0,"expected_outcome":[0,1,1]},
     "make_peace":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     }

ooo_a={"get_closer":{"w1":2,"w2":1,"expected_outcome":[1,1,1]},
     "express_happyness":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     "express_empathy":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     "make_peace":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     }

agreeableness_dict={
    "NT_N":{"weights":zzz_a,"num":[0,0,0]},
    "NT_S":{"weights":zzo_a,"num":[0,0,1]},
    "NT_A":{"weights":zoz_a,"num":[0,1,0]},
    "NT_H":{"weights":zoo_a,"num":[0,1,1]},
    "T_N":{"weights":ozz_a,"num":[1,0,0]},
    "T_S":{"weights":ozo_a,"num":[1,0,1]},
    "T_A":{"weights":ooz_a,"num":[1,1,0]},
    "T_H":{"weights":ooo_a,"num":[1,1,1]}
}



def choose_action_a(perception):
    global agree_actions, agreeableness_dict
    w=[]
    for a in agree_actions:
        
        weight=agreeableness_dict[perception]["weights"][a]["w1"]+agreeableness_dict[perception]["weights"][a]["w2"]
        w.append(float(weight))


    #print(w, sum(w),type(sum(w)))
    norm = [i/sum(w) for i in w]
   
    to_execute=np.random.choice(agree_actions,p=norm) #trovare il modo di normalizzare i pesi
    return to_execute, agreeableness_dict[perception]["weights"][to_execute]["w1"]+agreeableness_dict[perception]["weights"][to_execute]["w2"]



def update_weights_a(action, p_prev, p_after):
    list_real=agreeableness_dict[p_after]["num"]
    list_expected=agreeableness_dict[p_prev]["weights"][action]["expected_outcome"]
    error=0
    #accumulate the error between the perception and the expected one
    for i in range(0,len(list_real)):
        error+=(np.abs(list_real[i]-list_expected[i]))
    #normalize the error
    error=error/len(list_real)
    #update the weights
    prev=agreeableness_dict[p_prev]["weights"][action]["w2"]
    
    if error==0:
        agreeableness_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev+0.5),2)
        return agreeableness_dict[p_prev]["weights"][action]["w1"]+round(np.abs(prev + 0.5),2)
    else:
        if prev<0.1:
            return  prev+agreeableness_dict[p_prev]["weights"][action]["w1"]
        else:
           agreeableness_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev - 0.5),2)
           return round(np.abs(prev - 0.5),2)+agreeableness_dict[p_prev]["weights"][action]["w1"]