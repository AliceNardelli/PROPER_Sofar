#bits 00:neutral 01:sad 10:angry 11:happydict={}
#agreeable personality

import random
import numpy as np

agree_actions=["ask_if_can_it_be_useful","express_happyness_for_helping_the_user","express_empathy","affirm_to_mantain_the_calm_and_ask_if_can_be_useful"]

#GOAL make the user happy
#00 N 
#01 SA
#10 A, D, F
#11 H, SU

zz_a={"ask_if_can_it_be_useful":{"w1":4,"w2":2,"expected_outcome":[1,1]},
     "express_happyness_for_helping_the_user":{"w1":2,"w2":1,"expected_outcome":[1,1]},
     "express_empathy":{"w1":0,"w2":0,"expected_outcome":[1,1]},
     "affirm_to_mantain_the_calm_and_ask_if_can_be_useful":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0]},
     }

zo_a={"ask_if_can_it_be_useful":{"w1":2,"w2":1,"expected_outcome":[1,1]},
     "express_happyness_for_helping_the_user":{"w1":0,"w2":0,"expected_outcome":[1,1]},
     "express_empathy":{"w1":4,"w2":2,"expected_outcome":[1,1]},
     "affirm_to_mantain_the_calm_and_ask_if_can_be_useful":{"w1":0.0,"w2":0.0,"expected_outcome":[0,0]},
     }

oz_a={"ask_if_can_it_be_useful":{"w1":0,"w2":0,"expected_outcome":[1,1]},
     "express_happyness_for_helping_the_user":{"w1":0,"w2":0,"expected_outcome":[1,1]},
     "express_empathy":{"w1":2,"w2":1,"expected_outcome":[1,1]},
     "affirm_to_mantain_the_calm_and_ask_if_can_be_useful":{"w1":4,"w2":2,"expected_outcome":[1,1]},
     }

oo_a={"ask_if_can_it_be_useful":{"w1":2,"w2":1,"expected_outcome":[1,1]},
     "express_happyness_for_helping_the_user":{"w1":4,"w2":2,"expected_outcome":[1,1]},
     "express_empathy":{"w1":0.0,"w2":0.0,"expected_outcome":[1,1]},
     "affirm_to_mantain_the_calm_and_ask_if_can_be_useful":{"w1":0.0,"w2":0.0,"expected_outcome":[1,1]},
     }


agreeableness_dict={
    "N":{"weights":zz_a,"num":[0,0]},
    "S":{"weights":zo_a,"num":[0,1]},
    "A":{"weights":oz_a,"num":[1,0]},
    "H":{"weights":oo_a,"num":[1,1]}
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