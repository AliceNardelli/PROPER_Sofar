import json
import os
import random
import numpy as np


intro_actions=["say_if_can_be_useful",
               "ask_a_reflective_question",
               "say_that_you_are_there_to_listen_actively_the_human_thoughts",
               "say_that_you_prefer_confidential_conversation"]


zzz_i={"say_if_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "ask_a_reflective_question":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_are_there_to_listen_actively_the_human_thoughts":{"w1":4,"w2":2,"expected_outcome":[0,0,0]}, 
     "say_that_you_prefer_confidential_conversation":{"w1":4,"w2":2,"expected_outcome":[0,0,0]},
     }

zzo_i={"say_if_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "ask_a_reflective_question":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_are_there_to_listen_actively_the_human_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_prefer_confidential_conversation":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     }

zoz_i={"say_if_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "ask_a_reflective_question":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_are_there_to_listen_actively_the_human_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_prefer_confidential_conversation":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     }

zoo_i={"say_if_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "ask_a_reflective_question":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_are_there_to_listen_actively_the_human_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_prefer_confidential_conversation":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     }

ozz_i={"say_if_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "ask_a_reflective_question":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_are_there_to_listen_actively_the_human_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_prefer_confidential_conversation":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     }

ozo_i={"say_if_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "ask_a_reflective_question":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_are_there_to_listen_actively_the_human_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_prefer_confidential_conversation":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     }

ooz_i={"say_if_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "ask_a_reflective_question":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_are_there_to_listen_actively_the_human_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_prefer_confidential_conversation":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     }

ooo_i={"say_if_can_be_useful":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "ask_a_reflective_question":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_are_there_to_listen_actively_the_human_thoughts":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     "say_that_you_prefer_confidential_conversation":{"w1":6,"w2":2,"expected_outcome":[0,0,0]},
     }



default_introversion_dict={
    "NA_N":{"weights":zzz_i,"num":[0,0,0]},
    "NA_S":{"weights":zzo_i,"num":[0,0,1]},
    "NA_A":{"weights":zoz_i,"num":[0,1,0]},
    "NA_H":{"weights":zoo_i,"num":[0,1,1]},
    "A_N":{"weights":ozz_i,"num":[0,0,0]},
    "A_S":{"weights":ozo_i,"num":[0,0,1]},
    "A_A":{"weights":ooz_i,"num":[0,1,0]},
    "A_H":{"weights":ooo_i,"num":[0,1,1]},
}



def initialize_or_load_person_i(person_id):
    directory = f"/home/alice/EpisodicMemory/{person_id}/LE/"
    filename = os.path.join(directory, f"{person_id}.json")

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory
        print(f"Created directory: {directory}")
    
    # Initialize the JSON file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_introversion_dict, f, indent=4)
        print(f"Initialized data for {person_id}.")
    
    # Load and return the data from the file
    with open(filename, "r") as f:
        return json.load(f)
    

def save_person_data_i(person_id, data):
    directory = f"/home/alice/EpisodicMemory/{person_id}/LE/"
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
def choose_action_i(data, perception):
    weights = data[perception]["weights"]
    w = []
    for action in intro_actions:
        weight = weights[action]["w1"] + weights[action]["w2"]
        w.append(float(weight))
    norm = [i / sum(w) for i in w] if sum(w) != 0 else [1 / len(w)] * len(w)
    chosen_action = np.random.choice(intro_actions, p=norm)
    return chosen_action, weights[chosen_action]["w1"] + weights[chosen_action]["w2"]


# Update weights based on perception change
def update_weights_i(data, action, p_prev, p_after):
    list_real = data[p_after]["num"]
    list_expected = data[p_prev]["weights"][action]["expected_outcome"]
    error = sum(np.abs(np.array(list_real) - np.array(list_expected))) / len(list_real)
    prev_w2 = data[p_prev]["weights"][action]["w2"]

    if error == 0:
        data[p_prev]["weights"][action]["w2"] = round(prev_w2 + 0.5, 2)
    elif prev_w2 > 0.1:
        data[p_prev]["weights"][action]["w2"] = round(prev_w2 - 0.5, 2)
    return data, data[p_prev]["weights"][action]["w2"]+data[p_prev]["weights"][action]["w1"]
        

        