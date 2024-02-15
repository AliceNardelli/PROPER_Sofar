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
        "NA_N":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[0,0,0]},
        "NA_S":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[0,0,1]},
        "NA_A":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[0,1,0]},
        "NA_H":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[0,1,1]},
        "A_N":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[1,0,0]},
        "A_S":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[1,0,1]},
        "A_A":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[1,1,0]},
        "A_H":{"weights":rospy.get_param("zzz_u")[rospy.get_param("actual_goal")],"num":[1,1,1]}
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


