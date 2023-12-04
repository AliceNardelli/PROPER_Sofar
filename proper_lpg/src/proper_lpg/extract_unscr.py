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
import rospy
unsc_actions=[]

unsc_dict={}

def init_unsc_actions():
    global unsc_actions, unsc_dict
    unsc_actions=rospy.get_param("unsc_actions")[rospy.get_param("actual_goal")]
    unsc_dict={
        "NT_N":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[0,0,0]},
        "NT_S":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[0,0,1]},
        "NT_A":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[0,1,0]},
        "NT_H":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[0,1,1]},
        "T_N":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[1,0,0]},
        "T_S":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[1,0,1]},
        "T_A":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[1,1,0]},
        "T_H":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[1,1,1]}
    }



def choose_action_u(perception):
    global unsc_actions, unsc_dict
    w=[]
    for a in unsc_actions:
        
        weight=unsc_dict[perception]["weights"][a]["w1"]+unsc_dict[perception]["weights"][a]["w2"]
        w.append(float(weight))

    
    norm = [i/sum(w) for i in w]
    to_execute=np.random.choice(unsc_actions,p=norm) #trovare il modo di normalizzare i pesi
    return to_execute, unsc_dict[perception]["weights"][to_execute]["w1"]+unsc_dict[perception]["weights"][to_execute]["w2"]


"""
NO NEED OF UPDATING WEIGHTS
def update_weights_c(action, p_prev, p_after):
    list_real=unsc_dict[p_after]["num"]
    list_expected=unsc_dict[p_prev]["weights"][action]["expected_outcome"]
    error=0
    #accumulate the error between the perception and the expected one
    for i in range(0,len(list_real)):
        error+=(np.abs(list_real[i]-list_expected[i]))
    #normalize the error
    error=error/len(list_real)
    #update the weights
    prev=unsc_dict[p_prev]["weights"][action]["w2"]
    print("PREV", prev)
    if error==0:
        unsc_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev+0.1),2)
        print("AFTER", round(np.abs(prev+0.1),2))
        return round(np.abs(prev + 0.1),2)
    else:
        if prev<0.1:
            print("AFTER", prev)
            return  prev
        else:
           unsc_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev - 0.1),2)
           print("AFTER",round(np.abs(prev - 0.1),2))
           return round(np.abs(prev - 0.1),2)
"""