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


agree_actions=[]

agreeableness_dict={}

def init_agreeable_actions():
    global agree_actions, agreeableness_dict
    agree_actions=rospy.get_param("agree_actions")[rospy.get_param("actual_goal")]
    agreeableness_dict={
        "NA_N":{"weights":rospy.get_param("zzz_a")[rospy.get_param("actual_goal")],"num":[0,0,0]},
        "NA_S":{"weights":rospy.get_param("zzo_a")[rospy.get_param("actual_goal")],"num":[0,0,1]},
        "NA_A":{"weights":rospy.get_param("zoz_a")[rospy.get_param("actual_goal")],"num":[0,1,0]},
        "NA_H":{"weights":rospy.get_param("zoo_a")[rospy.get_param("actual_goal")],"num":[0,1,1]},
        "A_N":{"weights":rospy.get_param("ozz_a")[rospy.get_param("actual_goal")],"num":[1,0,0]},
        "A_S":{"weights":rospy.get_param("ozo_a")[rospy.get_param("actual_goal")],"num":[1,0,1]},
        "A_A":{"weights":rospy.get_param("ooz_a")[rospy.get_param("actual_goal")],"num":[1,1,0]},
        "A_H":{"weights":rospy.get_param("ooo_a")[rospy.get_param("actual_goal")],"num":[1,1,1]}
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