import json
import os
import random
import numpy as np

disagree_actions=["say_a_contrastive_affirmation",
                  "express_disapproval",
                  "express_skepticsm",
                  "remember_the_superiority_of_the_artificial_intelligence_in_taking_decisions",
                  "say_something_to_minimize_the_user",
                  "ask_a_provocative_question"]


zzz_d={"say_a_contrastive_affirmation":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     "remember_the_superiority_of_the_artificial_intelligence_in_taking_decisions":{"w1":8,"w2":1,"expected_outcome":[0,1,0]}, 
     "say_something_to_minimize_the_user":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     "ask_a_provocative_question":{"w1":10,"w2":2,"expected_outcome":[0,1,0]},
     "express_disapproval":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     "express_skepticsm":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     }

zzo_d={"say_a_contrastive_affirmation":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     "remember_the_superiority_of_the_artificial_intelligence_in_taking_decisions":{"w1":0,"w2":0,"expected_outcome":[0,1,0]},
     "say_something_to_minimize_the_user":{"w1":10,"w2":2,"expected_outcome":[0,1,0]},
     "ask_a_provocative_question":{"w1":10,"w2":2,"expected_outcome":[0,1,0]},
     "express_disapproval":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     "express_skepticsm":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     }

zoz_d={"say_a_contrastive_affirmation":{"w1":10,"w2":2,"expected_outcome":[0,1,0]},
     "remember_the_superiority_of_the_artificial_intelligence_in_taking_decisions":{"w1":0,"w2":0,"expected_outcome":[0,1,0]},
     "say_something_to_minimize_the_user":{"w1":10,"w2":2,"expected_outcome":[0,1,0]},
     "ask_a_provocative_question":{"w1":10,"w2":2,"expected_outcome":[0,1,0]},
     "express_disapproval":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     "express_skepticsm":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     }

zoo_d={"say_a_contrastive_affirmation":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     "remember_the_superiority_of_the_artificial_intelligence_in_taking_decisions":{"w1":10,"w2":2,"expected_outcome":[0,1,0]},
     "say_something_to_minimize_the_user":{"w1":10,"w2":2,"expected_outcome":[0,1,0]},
     "ask_a_provocative_question":{"w1":0.0,"w2":0.0,"expected_outcome":[0,1,0]},
     "express_disapproval":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     "express_skepticsm":{"w1":10,"w2":2,"expected_outcome":[0,1,0]},
     }

ozz_d={"say_a_contrastive_affirmation":{"w1":8,"w2":1,"expected_outcome":[1,1,0]},
     "remember_the_superiority_of_the_artificial_intelligence_in_taking_decisions":{"w1":8,"w2":1,"expected_outcome":[1,1,0]},
     "say_something_to_minimize_the_user":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     "ask_a_provocative_question":{"w1":0,"w2":0,"expected_outcome":[1,1,0]},
     "express_disapproval":{"w1":8,"w2":1,"expected_outcome":[1,1,0]},
     "express_skepticsm":{"w1":8,"w2":1,"expected_outcome":[1,1,0]},
     }

ozo_d={"say_a_contrastive_affirmation":{"w1":8,"w2":1,"expected_outcome":[1,1,0]},
     "remember_the_superiority_of_the_artificial_intelligence_in_taking_decisions":{"w1":10,"w2":2,"expected_outcome":[1,1,0]},
     "say_something_to_minimize_the_user":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     "ask_a_provocative_question":{"w1":0,"w2":0,"expected_outcome":[1,1,0]},
      "express_disapproval":{"w1":8,"w2":1,"expected_outcome":[1,1,0]},
     "express_skepticsm":{"w1":8,"w2":1,"expected_outcome":[1,1,0]},
     }

ooz_d={"say_a_contrastive_affirmation":{"w1":10,"w2":2,"expected_outcome":[1,1,0]},
     "remember_the_superiority_of_the_artificial_intelligence_in_taking_decisions":{"w1":8,"w2":1,"expected_outcome":[1,1,0]},
     "say_something_to_minimize_the_user":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     "ask_a_provocative_question":{"w1":0,"w2":0,"expected_outcome":[1,1,0]},
     "express_disapproval":{"w1":8,"w2":1,"expected_outcome":[1,1,0]},
     "express_skepticsm":{"w1":8,"w2":1,"expected_outcome":[1,1,0]},
     }

ooo_d={"say_a_contrastive_affirmation":{"w1":8,"w2":1,"expected_outcome":[1,1,0]},
     "remember_the_superiority_of_the_artificial_intelligence_in_taking_decisions":{"w1":10,"w2":2,"expected_outcome":[1,1,0]},
     "say_something_to_minimize_the_user":{"w1":8,"w2":1,"expected_outcome":[0,1,0]},
     "ask_a_provocative_question":{"w1":0.0,"w2":0.0,"expected_outcome":[1,1,0]},
     "express_disapproval":{"w1":8,"w2":1,"expected_outcome":[1,1,0]},
     "express_skepticsm":{"w1":8,"w2":1,"expected_outcome":[1,1,0]},
     }

default_disagreeableness_dict={
    "NA_N":{"weights":zzz_d,"num":[0,0,0]},
    "NA_S":{"weights":zzo_d,"num":[0,0,1]},
    "NA_A":{"weights":zoz_d,"num":[0,1,0]},
    "NA_H":{"weights":zoo_d,"num":[0,1,1]},
    "A_N":{"weights":ozz_d,"num":[1,0,0]},
    "A_S":{"weights":ozo_d,"num":[1,0,1]},
    "A_A":{"weights":ooz_d,"num":[1,1,0]},
    "A_H":{"weights":ooo_d,"num":[1,1,1]}
}




def initialize_or_load_person_d(person_id):
    directory = f"/home/alice/EpisodicMemory/{person_id}/LA/"
    filename = os.path.join(directory, f"{person_id}.json")

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory
        print(f"Created directory: {directory}")
    
    # Initialize the JSON file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_disagreeableness_dict, f, indent=4)
        print(f"Initialized data for {person_id}.")
    
    # Load and return the data from the file
    with open(filename, "r") as f:
        return json.load(f)
    

def save_person_data_d(person_id, data):
    directory = f"/home/alice/EpisodicMemory/{person_id}/LA/"
    filename = os.path.join(directory, f"{person_id}.json")

    # Ensure the directory exists before saving
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

    # Save the updated data to the file
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data for {person_id} has been saved.")


# Choose an action based on perception and sentence flag
def choose_action_d(data, perception):
    weights = data[perception]["weights"]
    w = []
    for action in disagree_actions:
        weight = weights[action]["w1"] + weights[action]["w2"]
        w.append(float(weight))
    norm = [i / sum(w) for i in w] if sum(w) != 0 else [1 / len(w)] * len(w)
    chosen_action = np.random.choice(disagree_actions, p=norm)
    return chosen_action, weights[chosen_action]["w1"] + weights[chosen_action]["w2"]


# Update weights based on perception change
def update_weights_d(data, action, p_prev, p_after):
    list_real = data[p_after]["num"]
    list_expected = data[p_prev]["weights"][action]["expected_outcome"]
    error = sum(np.abs(np.array(list_real) - np.array(list_expected))) / len(list_real)
    prev_w2 = data[p_prev]["weights"][action]["w2"]

    if error == 0:
        data[p_prev]["weights"][action]["w2"] = round(prev_w2 + 0.5, 2)
    elif prev_w2 > 0.1:
        data[p_prev]["weights"][action]["w2"] = round(prev_w2 - 0.5, 2)

    return data, data[p_prev]["weights"][action]["w2"]+data[p_prev]["weights"][action]["w1"]