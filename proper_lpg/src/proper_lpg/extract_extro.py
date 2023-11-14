#action1 avvicinarsi
#action2 esprimere entusiasmo
#action3 raccontare una barzelletta
#action4 attirare l'attenzione
#bit 1 0:not touch 1 bouch
#bit 2,3 00:neutral 01:sad 10:angry 11:happydict={}
#agreeable personality
from proper_lpg.load_ontology import *
import random
import numpy as np

extro_actions=["get_closer","express_enthusiasm","tell_a_joke","catch_the_attention"]


zzz_e={"get_closer":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "express_enthusiasm":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "tell_a_joke":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "catch_the_attention":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     }

zzo_e={"get_closer":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "express_enthusiasm":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "tell_a_joke":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "catch_the_attention":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

zoz_e={"get_closer":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "express_enthusiasm":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "tell_a_joke":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "catch_the_attention":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

zoo_e={"get_closer":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "express_enthusiasm":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "tell_a_joke":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     "catch_the_attention":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     }

ozz_e={"get_closer":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "express_enthusiasm":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "tell_a_joke":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "catch_the_attention":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     }

ozo_e={"get_closer":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "express_enthusiasm":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "tell_a_joke":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "catch_the_attention":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     }

ooz_e={"get_closer":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "express_enthusiasm":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0,0]},
     "tell_a_joke":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "catch_the_attention":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

ooo_e={"get_closer":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     "express_enthusiasm":{"w1":2,"w2":1,"expected_outcome":[0,0,0]},
     "tell_a_joke":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "catch_the_attention":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

extroversion_dict={
    "NT_N":{"weights":zzz_e,"num":[0,0,0]},
    "NT_S":{"weights":zzo_e,"num":[0,0,1]},
    "NT_A":{"weights":zoz_e,"num":[0,1,0]},
    "NT_H":{"weights":zoo_e,"num":[0,0,0]},
    "T_N":{"weights":ozz_e,"num":[1,0,0]},
    "T_S":{"weights":ozo_e,"num":[1,0,1]},
    "T_A":{"weights":ooz_e,"num":[1,1,0]},
    "T_H":{"weights":ooo_e,"num":[1,1,1]}
}



def choose_action_e(perception):
    global extro_actions, extroversion_dict
    w=[]
    for a in extro_actions:
        
        weight=extroversion_dict[perception]["weights"][a]["w1"]+extroversion_dict[perception]["weights"][a]["w2"]
        w.append(float(weight))

   
    norm = [i/sum(w) for i in w]
    to_execute=np.random.choice(extro_actions,p=norm) #trovare il modo di normalizzare i pesi
    return to_execute, extroversion_dict[perception]["weights"][to_execute]["w1"]+extroversion_dict[perception]["weights"][to_execute]["w2"]



def update_weights_e(action, p_prev, p_after):
    list_real=extroversion_dict[p_after]["num"]
    list_expected=extroversion_dict[p_prev]["weights"][action]["expected_outcome"]
    error=0
    #accumulate the error between the perception and the expected one
    for i in range(0,len(list_real)):
        error+=(np.abs(list_real[i]-list_expected[i]))
    #normalize the error
    error=error/len(list_real)
    #update the weights
    prev=extroversion_dict[p_prev]["weights"][action]["w2"]
    
    if error==0:
        extroversion_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev + 0.5),2)
        return round(np.abs(prev + 0.5),2)+extroversion_dict[p_prev]["weights"][action]["w1"]
    else:
        if prev<0.1:
            
            return  prev+extroversion_dict[p_prev]["weights"][action]["w1"]
        else:
           extroversion_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev - 0.5),2)
          
           return round(np.abs(prev - 0.5),2)+extroversion_dict[p_prev]["weights"][action]["w1"]
        

        