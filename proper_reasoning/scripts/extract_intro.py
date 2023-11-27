import random
import numpy as np

#GOAL avoid the human interaction, terminate the task cleanly
#00 N 
#01 SA
#10 A, D, F
#11 H, SU
intro_actions=["say_if_can_be_useful","say_to_proceed_in_their_task_or_terminate_the_conversation"]


zz_i={"say_if_can_be_useful":{"w1":4,"w2":2,"expected_outcome":[0,0]},
     "say_to_proceed_in_their_task_or_terminate_the_conversation":{"w1":4,"w2":2,"expected_outcome":[0,0]},
     }

zo_i={"say_if_can_be_useful":{"w1":4,"w2":2,"expected_outcome":[0,0]},
     "say_to_proceed_in_their_task_or_terminate_the_conversation":{"w1":4,"w2":2,"expected_outcome":[0,0]},
     }

oz_i={"say_if_can_be_useful":{"w1":4,"w2":2,"expected_outcome":[0,0]},
     "say_to_proceed_in_their_task_or_terminate_the_conversation":{"w1":4,"w2":2,"expected_outcome":[0,0]},
     }

oo_i={"say_if_can_be_useful":{"w1":4,"w2":2,"expected_outcome":[0,0]},
     "say_to_proceed_in_their_task_or_terminate_the_conversation":{"w1":4,"w2":2,"expected_outcome":[0,0]},
     }



introversion_dict={
    "N":{"weights":zz_i,"num":[0,0]},
    "S":{"weights":zo_i,"num":[0,1]},
    "A":{"weights":oz_i,"num":[1,0]},
    "H":{"weights":oo_i,"num":[0,0]},
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
        

        