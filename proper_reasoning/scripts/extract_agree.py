import json
import os
import random
import numpy as np

agree_actions=["say_a_compliment_to_the_user",
               "ask_if_it_can_be_useful",
               "comunicate_happyness_for_helping_the_user",
               "comunicate_empathy_to_the_user",
               "declare_to_mantain_the_calm_and_ask_if_can_be_useful",
               "ask_if_there_is_something_that_clouds_thoughts",
               "say_to_free_the_mind_from_thoughts",
               "say_to_be_glad_to_see_the_user_full_of_energy"]


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

default_agreeableness_dict={
    "NA_N":{"weights":zzz_a,"num":[0,0,0]},
    "NA_S":{"weights":zzo_a,"num":[0,0,1]},
    "NA_A":{"weights":zoz_a,"num":[0,1,0]},
    "NA_H":{"weights":zoo_a,"num":[0,1,1]},
    "A_N":{"weights":ozz_a,"num":[1,0,0]},
    "A_S":{"weights":ozo_a,"num":[1,0,1]},
    "A_A":{"weights":ooz_a,"num":[1,1,0]},
    "A_H":{"weights":ooo_a,"num":[1,1,1]}
}


def initialize_or_load_person_a(person_id):
    directory = f"/home/alice/EpisodicMemory/{person_id}/HA/"
    filename = os.path.join(directory, f"{person_id}.json")

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory
        print(f"Created directory: {directory}")
    
    # Initialize the JSON file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_agreeableness_dict, f, indent=4)
        print(f"Initialized data for {person_id}.")
    
    # Load and return the data from the file
    with open(filename, "r") as f:
        return json.load(f)
    

def save_person_data_a(person_id, data):
    directory = f"/home/alice/EpisodicMemory/{person_id}/HA/"
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
def choose_action_a(data, perception):
    weights = data[perception]["weights"]
    w = []
    for action in agree_actions:
        weight = weights[action]["w1"] + weights[action]["w2"]
        w.append(float(weight))
    norm = [i / sum(w) for i in w] if sum(w) != 0 else [1 / len(w)] * len(w)
    chosen_action = np.random.choice(agree_actions, p=norm)
    return chosen_action, weights[chosen_action]["w1"] + weights[chosen_action]["w2"]


# Update weights based on perception change
def update_weights_a(data, action, p_prev, p_after):
    list_real = data[p_after]["num"]
    list_expected = data[p_prev]["weights"][action]["expected_outcome"]
    error = sum(np.abs(np.array(list_real) - np.array(list_expected))) / len(list_real)
    prev_w2 = data[p_prev]["weights"][action]["w2"]

    if error == 0:
        data[p_prev]["weights"][action]["w2"] = round(prev_w2 + 0.5, 2)
    elif prev_w2 > 0.1:
        data[p_prev]["weights"][action]["w2"] = round(prev_w2 - 0.5, 2)

    return data, data[p_prev]["weights"][action]["w2"]+data[p_prev]["weights"][action]["w1"]