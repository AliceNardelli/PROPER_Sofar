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


disagree_actions=[]

disagreeableness_dict={}

def init_disagreeable_actions():
    global disagree_actions, disagreeableness_dict
    disagree_actions=rospy.get_param("disagree_actions")[rospy.get_param("actual_goal")]
    print(disagree_actions)
    disagreeableness_dict={
        "NA_N":{"weights":rospy.get_param("zzz_d")[rospy.get_param("actual_goal")],"num":[0,0,0]},
        "NA_S":{"weights":rospy.get_param("zzo_d")[rospy.get_param("actual_goal")],"num":[0,0,1]},
        "NA_A":{"weights":rospy.get_param("zoz_d")[rospy.get_param("actual_goal")],"num":[0,1,0]},
        "NA_H":{"weights":rospy.get_param("zoo_d")[rospy.get_param("actual_goal")],"num":[0,1,1]},
        "A_N":{"weights":rospy.get_param("zzz_d")[rospy.get_param("actual_goal")],"num":[1,0,0]},
        "A_S":{"weights":rospy.get_param("zzo_d")[rospy.get_param("actual_goal")],"num":[1,0,1]},
        "A_A":{"weights":rospy.get_param("zoz_d")[rospy.get_param("actual_goal")],"num":[1,1,0]},
        "A_H":{"weights":rospy.get_param("zoo_d")[rospy.get_param("actual_goal")],"num":[1,1,1]}
    }



def choose_action_d(perception):
    global disagree_actions, disagreeableness_dict
    w=[]
    for a in disagree_actions:
        
        weight=disagreeableness_dict[perception]["weights"][a]["w1"]+disagreeableness_dict[perception]["weights"][a]["w2"]
        w.append(float(weight))
    norm = [i/sum(w) for i in w]
    to_execute=np.random.choice(disagree_actions,p=norm) #trovare il modo di normalizzare i pesi
    return to_execute, disagreeableness_dict[perception]["weights"][to_execute]["w1"]+disagreeableness_dict[perception]["weights"][to_execute]["w2"]



def update_weights_d(action, p_prev, p_after):
    list_real=disagreeableness_dict[p_after]["num"]
    list_expected=disagreeableness_dict[p_prev]["weights"][action]["expected_outcome"]
    error=0
    
    for i in range(0,len(list_real)):
        error+=(np.abs(list_real[i]-list_expected[i]))
    #normalize the error
    error=error/len(list_real)
    #update the weights
    prev=disagreeableness_dict[p_prev]["weights"][action]["w2"]
    
    if error==0:
        disagreeableness_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev+0.5),2)
        return round(np.abs(prev + 0.5),2)+disagreeableness_dict[p_prev]["weights"][action]["w1"]
    else:
        if prev<0.1:
            return  prev +disagreeableness_dict[p_prev]["weights"][action]["w1"]
        else:
           disagreeableness_dict[p_prev]["weights"][action]["w2"]=round(np.abs(prev - 0.5),2)
           return round(np.abs(prev - 0.5),2)+disagreeableness_dict[p_prev]["weights"][action]["w1"]