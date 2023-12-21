#bits 00:neutral 01:sad 10:angry 11:happydict={}
#agreeable personality

import random
import numpy as np

agree_actions=["say_a_compliment_to_the_user","ask_if_it_can_be_useful","comunicate_happyness_for_helping_the_user","comunicate_empathy_to_the_user","declare_to_mantain_the_calm_and_ask_if_can_be_useful","ask_if_there_is_something_that_clouds_thoughts","say_to_free_the_mind_from_thoughts","say_to_be_glad_to_see_the_user_full_of_energy"]

#GOAL make the user happy
# the fisrt bit depend on the fact that the user has spoken
#00 N 
#01 SA
#10 A, D, F
#11 H, SU
#MODIFY THE PERCEIVED OUTPUT
zzz_a={"ask_if_it_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "say_a_compliment_to_the_user":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "comunicate_happyness_for_helping_the_user":{"w1":4,"w2":1,"expected_outcome":[0,1,1]},
     "comunicate_empathy_to_the_user":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     "declare_to_mantain_the_calm_and_ask_if_can_be_useful":{"w1":0.0,"w2":0.0,"expected_outcome":[0,1,1]},
     "ask_if_there_is_something_that_clouds_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "say_to_free_the_mind_from_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "say_to_be_glad_to_see_the_user_full_of_energy":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     }

zzo_a={"ask_if_it_can_be_useful":{"w1":4,"w2":1,"expected_outcome":[0,1,1]},
       "say_a_compliment_to_the_user":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "comunicate_happyness_for_helping_the_user":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     "comunicate_empathy_to_the_user":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "declare_to_mantain_the_calm_and_ask_if_can_be_useful":{"w1":0.0,"w2":0.0,"expected_outcome":[0,1,1]},
     "ask_if_there_is_something_that_clouds_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "say_to_free_the_mind_from_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "say_to_be_glad_to_see_the_user_full_of_energy":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     }

zoz_a={"ask_if_it_can_be_useful":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     "say_a_compliment_to_the_user":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "comunicate_happyness_for_helping_the_user":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     "comunicate_empathy_to_the_user":{"w1":4,"w2":1,"expected_outcome":[0,1,1]},
     "declare_to_mantain_the_calm_and_ask_if_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "ask_if_there_is_something_that_clouds_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "say_to_free_the_mind_from_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "say_to_be_glad_to_see_the_user_full_of_energy":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     }

zoo_a={"ask_if_it_can_be_useful":{"w1":4,"w2":1,"expected_outcome":[0,1,1]},
       "say_a_compliment_to_the_user":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "comunicate_happyness_for_helping_the_user":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "comunicate_empathy_to_the_user":{"w1":0.0,"w2":0.0,"expected_outcome":[0,1,1]},
     "declare_to_mantain_the_calm_and_ask_if_can_be_useful":{"w1":0.0,"w2":0.0,"expected_outcome":[0,1,1]},
     "ask_if_there_is_something_that_clouds_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "say_to_free_the_mind_from_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,1,1]},
     "say_to_be_glad_to_see_the_user_full_of_energy":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     }

ozz_a={"ask_if_it_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_a_compliment_to_the_user":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "comunicate_happyness_for_helping_the_user":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "comunicate_empathy_to_the_user":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "declare_to_mantain_the_calm_and_ask_if_can_be_useful":{"w1":0.0,"w2":0.0,"expected_outcome":[1,1,1]},
     "ask_if_there_is_something_that_clouds_thoughts":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "say_to_free_the_mind_from_thoughts":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "say_to_be_glad_to_see_the_user_full_of_energy":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     }

ozo_a={"ask_if_it_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_a_compliment_to_the_user":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "comunicate_happyness_for_helping_the_user":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     "comunicate_empathy_to_the_user":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "declare_to_mantain_the_calm_and_ask_if_can_be_useful":{"w1":0.0,"w2":0.0,"expected_outcome":[1,1,1]},
     "ask_if_there_is_something_that_clouds_thoughts":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_to_free_the_mind_from_thoughts":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_to_be_glad_to_see_the_user_full_of_energy":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     }

ooz_a={"ask_if_it_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_a_compliment_to_the_user":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "comunicate_happyness_for_helping_the_user":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     "comunicate_empathy_to_the_user":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "declare_to_mantain_the_calm_and_ask_if_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "ask_if_there_is_something_that_clouds_thoughts":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_to_free_the_mind_from_thoughts":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_to_be_glad_to_see_the_user_full_of_energy":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     }

ooo_a={"ask_if_it_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_a_compliment_to_the_user":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "comunicate_happyness_for_helping_the_user":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "comunicate_empathy_to_the_user":{"w1":0.0,"w2":0.0,"expected_outcome":[1,1,1]},
     "declare_to_mantain_the_calm_and_ask_if_can_be_useful":{"w1":0.0,"w2":0.0,"expected_outcome":[1,1,1]},
     "ask_if_there_is_something_that_clouds_thoughts":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     "say_to_free_the_mind_from_thoughts":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     "say_to_be_glad_to_see_the_user_full_of_energy":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     }

agreeableness_dict={
    "NA_N":{"weights":zzz_a,"num":[0,0,0]},
    "NA_S":{"weights":zzo_a,"num":[0,0,1]},
    "NA_A":{"weights":zoz_a,"num":[0,1,0]},
    "NA_H":{"weights":zoo_a,"num":[0,1,1]},
    "A_N":{"weights":ozz_a,"num":[1,0,0]},
    "A_S":{"weights":ozo_a,"num":[1,0,1]},
    "A_A":{"weights":ooz_a,"num":[1,1,0]},
    "A_H":{"weights":ooo_a,"num":[1,1,1]}
}


def choose_action_a(perception, sentence):
    global agree_actions, agreeableness_dict
    w=[]
    for a in agree_actions:
        if ("ask"in a) and (sentence==True):
          weight=0
        else:
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