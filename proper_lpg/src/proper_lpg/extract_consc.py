

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
        "A_N":{"weights":rospy.get_param("zzz_c")[rospy.get_param("actual_goal")],"num":[1,0,0]},
        "A_S":{"weights":rospy.get_param("zzz_c")[rospy.get_param("actual_goal")],"num":[1,0,1]},
        "A_A":{"weights":rospy.get_param("zoz_c")[rospy.get_param("actual_goal")],"num":[1,1,0]},
        "A_H":{"weights":rospy.get_param("zzz_c")[rospy.get_param("actual_goal")],"num":[1,1,1]}
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


