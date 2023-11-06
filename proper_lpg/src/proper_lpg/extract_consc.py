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

consc_actions=["say_to_focus_on_long_term","say_to_understand_your_objective","be_calm"]


zzz_c={"say_to_focus_on_long_term":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_understand_your_objective":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "be_calm":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

zzo_c={"say_to_focus_on_long_term":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_understand_your_objective":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "be_calm":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

zoz_c={"say_to_focus_on_long_term":{"w1":2,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_understand_your_objective":{"w1":2,"w2":0,"expected_outcome":[0,0,0]},
     "be_calm":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

zoo_c={"say_to_focus_on_long_term":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_understand_your_objective":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "be_calm":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

ozz_c={"say_to_focus_on_long_term":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_understand_your_objective":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "be_calm":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

ozo_c={"say_to_focus_on_long_term":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_understand_your_objective":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "be_calm":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

ooz_c={"say_to_focus_on_long_term":{"w1":2,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_understand_your_objective":{"w1":2,"w2":0,"expected_outcome":[0,0,0]},
     "be_calm":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

ooo_c={"say_to_focus_on_long_term":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_understand_your_objective":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "be_calm":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

consc_dict={
    "NT_N":{"weights":zzz_c,"num":[0,0,0]},
    "NT_S":{"weights":zzo_c,"num":[0,0,1]},
    "NT_A":{"weights":zoz_c,"num":[0,1,0]},
    "NT_H":{"weights":zoo_c,"num":[0,1,1]},
    "T_N":{"weights":ozz_c,"num":[1,0,0]},
    "T_S":{"weights":ozo_c,"num":[1,0,1]},
    "T_A":{"weights":ooz_c,"num":[1,1,0]},
    "T_H":{"weights":ooo_c,"num":[1,1,1]}
}



def choose_action_c(perception):
    global consc_actions, consc_dict
    w=[]
    for a in consc_actions:
        print(a)
        weight=consc_dict[perception]["weights"][a]["w1"]+consc_dict[perception]["weights"][a]["w2"]
        w.append(float(weight))

    print(w[0])
    #print(w, sum(w),type(sum(w)))
    norm = [i/sum(w) for i in w]
    print(norm)
    to_execute=np.random.choice(consc_actions,p=norm) #trovare il modo di normalizzare i pesi
    return to_execute, consc_dict[perception]["weights"][to_execute]["w1"]+consc_dict[perception]["weights"][to_execute]["w2"]


"""
NO NEED OF UPDATING WEIGHTS
def update_weights_c(action, p_prev, p_after):
    list_real=consc_dict[p_after]["num"]
    list_expected=consc_dict[p_prev]["weights"][action]["expected_outcome"]
    error=0
    #accumulate the error between the perception and the expected one
    for i in range(0,len(list_real)):
        error+=(np.abs(list_real[i]-list_expected[i]))
    #normalize the error
    error=error/len(list_real)
    #update the weights
    prev=consc_dict[p_prev]["weights"][action]["w2"]
    print("PREV", prev)
    if error==0:
        consc_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev+0.1),2)
        print("AFTER", round(np.abs(prev+0.1),2))
        return round(np.abs(prev + 0.1),2)
    else:
        if prev<0.1:
            print("AFTER", prev)
            return  prev
        else:
           consc_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev - 0.1),2)
           print("AFTER",round(np.abs(prev - 0.1),2))
           return round(np.abs(prev - 0.1),2)
"""