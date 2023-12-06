import random
import numpy as np

#GOAL focus on long term goals
#00 N 
#01 SA
#10 A, D, F
#11 H, SU

unsc_actions=["distract_the_user_with_a_random_question","make_a_thoughtless_consideration"]


zzz_u={"distract_the_user_with_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

zzo_u={"distract_the_user_with_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

zoz_u={"distract_the_user_with_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

zoo_u={"distract_the_user_with_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

ozz_u={"distract_the_user_with_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

ozo_u={"distract_the_user_with_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

ooz_u={"distract_the_user_with_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

ooo_u={"distract_the_user_with_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

unsc_dict={
    "NS_N":{"weights":zzz_u,"num":[0,0,0]},
    "NS_S":{"weights":zzo_u,"num":[0,0,1]},
    "NS_A":{"weights":zoz_u,"num":[0,1,0]},
    "NS_H":{"weights":zoo_u,"num":[0,1,1]},
    "S_N":{"weights":ozz_u,"num":[0,0,0]},
    "S_S":{"weights":ozo_u,"num":[0,0,1]},
    "S_A":{"weights":ooz_u,"num":[0,1,0]},
    "S_H":{"weights":ooo_u,"num":[0,1,1]},
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


