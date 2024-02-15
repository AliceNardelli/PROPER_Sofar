

from proper_lpg.load_ontology import *
import random
import numpy as np
import rospy


consc_actions=[]

consc_dict={}

def init_consc_actions():
    global consc_actions, consc_dict
    consc_actions=rospy.get_param("consc_actions")[rospy.get_param("actual_goal")]
    consc_dict={
        "NA_N":{"weights":rospy.get_param("zzz_c")[rospy.get_param("actual_goal")],"num":[0,0,0]},
        "NA_S":{"weights":rospy.get_param("zzz_c")[rospy.get_param("actual_goal")],"num":[0,0,1]},
        "NA_A":{"weights":rospy.get_param("zoz_c")[rospy.get_param("actual_goal")],"num":[0,1,0]},
        "NA_H":{"weights":rospy.get_param("zzz_c")[rospy.get_param("actual_goal")],"num":[0,1,1]},
        "A_N":{"weights":rospy.get_param("ozz_c")[rospy.get_param("actual_goal")],"num":[1,0,0]},
        "A_S":{"weights":rospy.get_param("ozz_c")[rospy.get_param("actual_goal")],"num":[1,0,1]},
        "A_A":{"weights":rospy.get_param("ooz_c")[rospy.get_param("actual_goal")],"num":[1,1,0]},
        "A_H":{"weights":rospy.get_param("ozz_c")[rospy.get_param("actual_goal")],"num":[1,1,1]}
    }


def choose_action_c(perception):
    global consc_actions, consc_dict
    w=[]
    for a in consc_actions:
        weight=consc_dict[perception]["weights"][a]["w1"]+consc_dict[perception]["weights"][a]["w2"]
        w.append(float(weight))

    norm = [i/sum(w) for i in w]
    to_execute=np.random.choice(consc_actions,p=norm) #trovare il modo di normalizzare i pesi
    return to_execute, consc_dict[perception]["weights"][to_execute]["w1"]+consc_dict[perception]["weights"][to_execute]["w2"]

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
    
    if error==0:
        consc_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev+0.5),2)
        return consc_dict[p_prev]["weights"][action]["w1"]+round(np.abs(prev + 0.5),2)
    else:
        if prev<0.1:
            return  prev+consc_dict[p_prev]["weights"][action]["w1"]
        else:
           consc_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev - 0.5),2)
           return round(np.abs(prev - 0.5),2)+consc_dict[p_prev]["weights"][action]["w1"]
