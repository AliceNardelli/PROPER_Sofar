#action1 allontanarsi
#action2 distogliere lo sguardo
#action3 guardare in basso e girarsi
#action4 non reagire
#bit 1 0:not touch 1 bouch
#bit 2,3 00:neutral 01:sad 10:angry 11:happydict={}
#agreeable personality
from proper_lpg.load_ontology import *
import random
import numpy as np

intro_actions=["a1","a2","a3","a4"]


zzz_i={"a1":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "a2":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "a3":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "a4":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     }

zzo_i={"a1":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "a2":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "a3":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "a4":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

zoz_i={"a1":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "a2":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "a3":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "a4":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

zoo_i={"a1":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "a2":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "a3":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     "a4":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     }

ozz_i={"a1":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "a2":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "a3":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "a4":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     }

ozo_i={"a1":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "a2":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "a3":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "a4":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     }

ooz_i={"a1":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "a2":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     "a3":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "a4":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

ooo_i={"a1":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "a2":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "a3":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "a4":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
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
        print(a)
        weight=introversion_dict[perception]["weights"][a]["w1"]+introversion_dict[perception]["weights"][a]["w2"]
        w.append(float(weight))

    print(w[0])
    #print(w, sum(w),type(sum(w)))
    norm = [i/sum(w) for i in w]
    print(norm)
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
    print("PREV", prev)
    if error==0:
        introversion_dict[p_prev]["weights"][action]["w2"]=np.abs(prev+0.1)
        print("AFTER", np.abs(prev+0.1))
        return prev + 0.1
    else:
        if prev<0.1:
            print("AFTER", prev)
            return  prev
        else:
           introversion_dict[p_prev]["weights"][action]["w2"]=np.abs(prev-0.1)
           print("AFTER", np.abs(prev-0.1))
           return prev - 0.1