import random
import numpy as np

#GOAL obtain social attention
#00 N 
#01 SA
#10 A, D, F
#11 H, SU
extro_actions=["say_an_enthusiastic_sentence","say_something_funny","ask_a_question"]


zzz_e={"say_an_enthusiastic_sentence":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     "say_something_funny":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "ask_a_question":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     }

zzo_e={"say_an_enthusiastic_sentence":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     "say_something_funny":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     "ask_a_question":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     }

zoz_e={"say_an_enthusiastic_sentence":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "say_something_funny":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "ask_a_question":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     }

zoo_e={"say_an_enthusiastic_sentence":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     "say_something_funny":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     "ask_a_question":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     }

ozz_e={"say_an_enthusiastic_sentence":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     "say_something_funny":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "ask_a_question":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     }

ozo_e={"say_an_enthusiastic_sentence":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     "say_something_funny":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     "ask_a_question":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     }

ooz_e={"say_an_enthusiastic_sentence":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "say_something_funny":{"w1":2,"w2":1,"expected_outcome":[0,1,1]},
     "ask_a_question":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     }

ooo_e={"say_an_enthusiastic_sentence":{"w1":4,"w2":2,"expected_outcome":[0,1,1]},
     "say_something_funny":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     "ask_a_question":{"w1":0,"w2":0,"expected_outcome":[0,1,1]},
     }


extroversion_dict={
    "NS_N":{"weights":zzz_e,"num":[0,0,0]},
    "NS_S":{"weights":zzo_e,"num":[0,0,1]},
    "NS_A":{"weights":zoz_e,"num":[0,1,0]},
    "NS_H":{"weights":zoo_e,"num":[0,1,1]},
    "S_N":{"weights":ozz_e,"num":[0,0,0]},
    "S_S":{"weights":ozo_e,"num":[0,0,1]},
    "S_A":{"weights":ooz_e,"num":[0,1,0]},
    "S_H":{"weights":ooo_e,"num":[0,1,1]},
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
        

        