import random
import numpy as np

#GOAL focus on long term goals
#00 N 
#01 SA
#10 A, D, F
#11 H, SU

unsc_actions=["distract_the_user_asking_a_random_question","make_a_thoughtless_consideration","say_that_sometimes_it_is_important_to_take_off_your_head", "say_that_it_is_nice_to_find_someone_with_its_head_in_the_clouds","say_something_inconsistent"]


zzz_u={"distract_the_user_asking_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_that_sometimes_it_is_important_to_take_off_your_head":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "say_that_it_is_nice_to_find_someone_with_its_head_in_the_clouds":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_inconsistent":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

zzo_u={"distract_the_user_asking_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_that_sometimes_it_is_important_to_take_off_your_head":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "say_that_it_is_nice_to_find_someone_with_its_head_in_the_clouds":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_inconsistent":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }


zoz_u={"distract_the_user_asking_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_that_sometimes_it_is_important_to_take_off_your_head":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
     "say_that_it_is_nice_to_find_someone_with_its_head_in_the_clouds":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_inconsistent":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }


zoo_u={"distract_the_user_asking_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_that_sometimes_it_is_important_to_take_off_your_head":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
      "say_that_it_is_nice_to_find_someone_with_its_head_in_the_clouds":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
      "say_something_inconsistent":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

ozz_u={"distract_the_user_asking_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_that_sometimes_it_is_important_to_take_off_your_head":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
      "say_that_it_is_nice_to_find_someone_with_its_head_in_the_clouds":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
      "say_something_inconsistent":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

ozo_u={"distract_the_user_asking_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_that_sometimes_it_is_important_to_take_off_your_head":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
      "say_that_it_is_nice_to_find_someone_with_its_head_in_the_clouds":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
      "say_something_inconsistent":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

ooz_u={"distract_the_user_asking_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_that_sometimes_it_is_important_to_take_off_your_head":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
      "say_that_it_is_nice_to_find_someone_with_its_head_in_the_clouds":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
      "say_something_inconsistent":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

ooo_u={"distract_the_user_asking_a_random_question":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     "say_that_sometimes_it_is_important_to_take_off_your_head":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
      "say_that_it_is_nice_to_find_someone_with_its_head_in_the_clouds":{"w1":0,"w2":0,"expected_outcome":[0,0,0]},
      "say_something_inconsistent":{"w1":4,"w2":0,"expected_outcome":[0,0,0]},
     }

unsc_dict={
    "NA_N":{"weights":zzz_u,"num":[0,0,0]},
    "NA_S":{"weights":zzo_u,"num":[0,0,1]},
    "NA_A":{"weights":zoz_u,"num":[0,1,0]},
    "NA_H":{"weights":zoo_u,"num":[0,1,1]},
    "A_N":{"weights":ozz_u,"num":[0,0,0]},
    "A_S":{"weights":ozo_u,"num":[0,0,1]},
    "A_A":{"weights":ooz_u,"num":[0,1,0]},
    "A_H":{"weights":ooo_u,"num":[0,1,1]},
}



def choose_action_u(perception, sentence):
    global unsc_actions, unsc_dict
    w=[]
    for a in unsc_actions:
        if (sentence==True) and ("ask" in a):
            weight=0
        else:
            weight=unsc_dict[perception]["weights"][a]["w1"]+unsc_dict[perception]["weights"][a]["w2"]
        w.append(float(weight))

    
    norm = [i/sum(w) for i in w]
    to_execute=np.random.choice(unsc_actions,p=norm) #trovare il modo di normalizzare i pesi
    return to_execute, unsc_dict[perception]["weights"][to_execute]["w1"]+unsc_dict[perception]["weights"][to_execute]["w2"]


