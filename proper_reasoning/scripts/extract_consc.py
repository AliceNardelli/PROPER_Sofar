import random
import numpy as np

#GOAL focus on long term goals
#00 N 
#01 SA
#10 A, D, F
#11 H, SU

consc_actions=["say_the_user_to_focus_on_long_term_goals_and_not_waste_time","ask_where_it_can_be_useful","say_to_be_focused","remind_to_not_distract","say_something_to_promote_ethical_behavior","ask_the_user_if_it_can_offer_guidance"]


zzz_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_be_focused":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "remind_to_not_distract":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     }

zzo_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_be_focused":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "remind_to_not_distract":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     }

zoz_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_be_focused":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "remind_to_not_distract":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
    
     }

zoo_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "ask_where_it_can_be_useful":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_be_focused":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "remind_to_not_distract":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     }

ozz_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_be_focused":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "remind_to_not_distract":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     }

ozo_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_be_focused":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "remind_to_not_distract":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

ooz_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_be_focused":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "remind_to_not_distract":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
    
     }

ooo_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[0,0,0]},
     "say_to_be_focused":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "remind_to_not_distract":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }




consc_dict={
    "NA_N":{"weights":zzz_c,"num":[0,0]},
    "NA_S":{"weights":zzo_c,"num":[0,1]},
    "NA_A":{"weights":zoz_c,"num":[1,0]},
    "NA_H":{"weights":zoo_c,"num":[1,1]},
    "A_N":{"weights":ozz_c,"num":[0,0]},
    "A_S":{"weights":ozo_c,"num":[0,1]},
    "A_A":{"weights":ooz_c,"num":[1,0]},
    "A_H":{"weights":ooo_c,"num":[1,1]},
}



def choose_action_c(perception,sentence):
    global consc_actions, consc_dict
    w=[]
    for a in consc_actions:
        if (sentence==True) and "ask" in a:
            weight=0
        else:
            weight=consc_dict[perception]["weights"][a]["w1"]+consc_dict[perception]["weights"][a]["w2"]
        w.append(float(weight))

    norm = [i/sum(w) for i in w]
    to_execute=np.random.choice(consc_actions,p=norm) #trovare il modo di normalizzare i pesi
    return to_execute, consc_dict[perception]["weights"][to_execute]["w1"]+consc_dict[perception]["weights"][to_execute]["w2"]

