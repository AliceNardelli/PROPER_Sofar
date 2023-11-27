import random
import numpy as np

disagree_actions=["say_a_contrastive_affirmation","remember_the_superiority_of_an_artificial_intelligence_in_taking_decisions","triggering_the_user_with_a_provocative_question"]

#GOAL make the user angry, create cometitiveness
#00 N 
#01 SA
#10 A, D, F
#11 H, SU

zz_d={"say_a_contrastive_affirmation":{"w1":2,"w2":1,"expected_outcome":[1,0]},
     "remember_the_superiority_of_an_artificial_intelligence_in_taking_decisions":{"w1":2,"w2":1,"expected_outcome":[1,0]},
     "triggering_the_user_with_a_provocative_question":{"w1":2,"w2":1,"expected_outcome":[1,0]},
     }

zo_d={"say_a_contrastive_affirmation":{"w1":2,"w2":1,"expected_outcome":[1,0]},
     "remember_the_superiority_of_an_artificial_intelligence_in_taking_decisions":{"w1":4,"w2":2,"expected_outcome":[1,0]},
     "triggering_the_user_with_a_provocative_question":{"w1":2,"w2":1,"expected_outcome":[1,0]},
     }

oz_d={"say_a_contrastive_affirmation":{"w1":4,"w2":2,"expected_outcome":[1,0]},
     "remember_the_superiority_of_an_artificial_intelligence_in_taking_decisions":{"w1":2,"w2":1,"expected_outcome":[1,0]},
     "triggering_the_user_with_a_provocative_question":{"w1":4,"w2":2,"expected_outcome":[1,0]},
     }

oo_d={"say_a_contrastive_affirmation":{"w1":2,"w2":1,"expected_outcome":[1,0]},
     "remember_the_superiority_of_an_artificial_intelligence_in_taking_decisions":{"w1":4,"w2":2,"expected_outcome":[1,0]},
     "triggering_the_user_with_a_provocative_question":{"w1":0.0,"w2":0.0,"expected_outcome":[1,0]},
     }


disagreeableness_dict={
    "N":{"weights":zz_d,"num":[0,0]},
    "S":{"weights":zo_d,"num":[0,1]},
    "A":{"weights":oz_d,"num":[1,0]},
    "H":{"weights":oo_d,"num":[1,1]}
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