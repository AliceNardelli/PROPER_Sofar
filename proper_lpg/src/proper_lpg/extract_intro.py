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
import rospy 

intro_actions=[]
introversion_dict={}

def init_intro_actions():
     global intro_actions, introversion_dict
     intro_actions=rospy.get_param("intro_actions")[rospy.get_param("actual_goal")]



     introversion_dict={
     "NA_N":{"weights":rospy.get_param("zzz_i")[rospy.get_param("actual_goal")],"num":[0,0,0]},
     "NA_S":{"weights":rospy.get_param("zzo_i")[rospy.get_param("actual_goal")],"num":[0,0,1]},
     "NA_A":{"weights":rospy.get_param("zoz_i")[rospy.get_param("actual_goal")],"num":[0,1,0]},
     "NA_H":{"weights":rospy.get_param("zoo_i")[rospy.get_param("actual_goal")],"num":[0,1,1]},
     "A_N":{"weights":rospy.get_param("ozz_i")[rospy.get_param("actual_goal")],"num":[1,0,0]},
     "A_S":{"weights":rospy.get_param("ozo_i")[rospy.get_param("actual_goal")],"num":[1,0,1]},
     "A_A":{"weights":rospy.get_param("ooz_i")[rospy.get_param("actual_goal")],"num":[1,1,0]},
     "A_H":{"weights":rospy.get_param("ooo_i")[rospy.get_param("actual_goal")],"num":[1,1,1]}
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
        

        