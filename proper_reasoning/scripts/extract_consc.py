import random
import numpy as np

#GOAL focus on long term goals
#00 N 
#01 SA
#10 A, D, F
#11 H, SU

consc_actions=["say_the_user_to_focus_on_long_term_goals_and_not_waste_time","ask_where_it_can_be_useful"]


zz_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "ask_where_it_can_be_useful":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

zo_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":2,"w2":0,"expected_outcome":[0,0,0]},
     "ask_where_it_can_be_useful":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

oz_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "ask_where_it_can_be_useful":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
    
     }

oo_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "ask_where_it_can_be_useful":{"w1":2,"w2":0,"expected_outcome":[0,0,0]},
     }


consc_dict={
    "N":{"weights":zz_c,"num":[0,0]},
    "S":{"weights":zo_c,"num":[0,1]},
    "A":{"weights":oz_c,"num":[1,0]},
    "H":{"weights":oo_c,"num":[1,1]},
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

