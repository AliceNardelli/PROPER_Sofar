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
import rospy 

extro_actions=[]
extroversion_dict={}

def init_extro_actions():
     global extro_actions, extroversion_dict
     extro_actions=rospy.get_param("extro_actions")[rospy.get_param("actual_goal")]



     extroversion_dict={
     "NT_N":{"weights":rospy.get_param("zzz_e")[rospy.get_param("actual_goal")],"num":[0,0,0]},
     "NT_S":{"weights":rospy.get_param("zzo_e")[rospy.get_param("actual_goal")],"num":[0,0,1]},
     "NT_A":{"weights":rospy.get_param("zoz_e")[rospy.get_param("actual_goal")],"num":[0,1,0]},
     "NT_H":{"weights":rospy.get_param("zoo_e")[rospy.get_param("actual_goal")],"num":[0,1,1]},
     "T_N":{"weights":rospy.get_param("ozz_e")[rospy.get_param("actual_goal")],"num":[1,0,0]},
     "T_S":{"weights":rospy.get_param("ozo_e")[rospy.get_param("actual_goal")],"num":[1,0,1]},
     "T_A":{"weights":rospy.get_param("ooz_e")[rospy.get_param("actual_goal")],"num":[1,1,0]},
     "T_H":{"weights":rospy.get_param("ooo_e")[rospy.get_param("actual_goal")],"num":[1,1,1]}
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
        

        