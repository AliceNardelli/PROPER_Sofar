import json
import os
import random
import numpy as np


consc_actions=["say_the_user_to_focus_on_long_term_goals_and_not_waste_time",
               "ask_where_it_can_be_useful","say_to_be_focused",
               "remind_to_not_distract",
               "say_something_to_promote_ethical_behavior",
               "ask_the_user_if_it_can_offer_guidance"]


zzz_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_to_be_focused":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "remind_to_not_distract":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     }

zzo_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":4,"w2":0,"expected_outcome":[1,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_to_be_focused":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "remind_to_not_distract":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     }

zoz_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_to_be_focused":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "remind_to_not_distract":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
    
     }

zoo_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "ask_where_it_can_be_useful":{"w1":4,"w2":0,"expected_outcome":[1,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_to_be_focused":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "remind_to_not_distract":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     }

ozz_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_to_be_focused":{"w1":0,"w2":0,"expected_outcome":[1,0,0]},
     "remind_to_not_distract":{"w1":0,"w2":0,"expected_outcome":[1,0,0]},
     }

ozo_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":4,"w2":0,"expected_outcome":[1,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_to_be_focused":{"w1":4,"w2":0,"expected_outcome":[1,0,0]},
     "remind_to_not_distract":{"w1":4,"w2":0,"expected_outcome":[1,0,0]},
     }

ooz_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_to_be_focused":{"w1":4,"w2":0,"expected_outcome":[1,0,0]},
     "remind_to_not_distract":{"w1":4,"w2":0,"expected_outcome":[1,0,0]},
    
     }

ooo_c={"say_the_user_to_focus_on_long_term_goals_and_not_waste_time":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "ask_where_it_can_be_useful":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "ask_the_user_if_it_can_offer_guidance":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_something_to_promote_ethical_behavior":{"w1":6,"w2":0,"expected_outcome":[1,0,0]},
     "say_to_be_focused":{"w1":4,"w2":0,"expected_outcome":[1,0,0]},
     "remind_to_not_distract":{"w1":4,"w2":0,"expected_outcome":[1,0,0]},
     }




default_consc_dict={
    "NA_N":{"weights":zzz_c,"num":[0,0,0]},
    "NA_S":{"weights":zzo_c,"num":[0,0,1]},
    "NA_A":{"weights":zoz_c,"num":[0,1,0]},
    "NA_H":{"weights":zoo_c,"num":[0,1,1]},
    "A_N":{"weights":ozz_c,"num":[1,0,0]},
    "A_S":{"weights":ozo_c,"num":[1,0,1]},
    "A_A":{"weights":ooz_c,"num":[1,1,0]},
    "A_H":{"weights":ooo_c,"num":[1,1,1]},
}



def initialize_or_load_person_c(person_id):
    directory = f"/home/alice/EpisodicMemory/{person_id}/HC/"
    filename = os.path.join(directory, f"{person_id}.json")

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory
        print(f"Created directory: {directory}")
    
    # Initialize the JSON file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_consc_dict, f, indent=4)
        print(f"Initialized data for {person_id}.")
    
    # Load and return the data from the file
    with open(filename, "r") as f:
        return json.load(f)
    

def save_person_data_c(person_id, data):
    directory = f"/home/alice/EpisodicMemory/{person_id}/HC/"
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
def choose_action_c(data, perception):
    weights = data[perception]["weights"]
    w = []
    for action in consc_actions:
        weight = weights[action]["w1"] + weights[action]["w2"]
        w.append(float(weight))
    norm = [i / sum(w) for i in w] if sum(w) != 0 else [1 / len(w)] * len(w)
    chosen_action = np.random.choice(consc_actions, p=norm)
    return chosen_action, weights[chosen_action]["w1"] + weights[chosen_action]["w2"]


# Update weights based on perception change
def update_weights_c(data, action, p_prev, p_after):
    list_real = [data[p_after]["num"][0]]
    list_expected = [data[p_prev]["weights"][action]["expected_outcome"][0]]
    error = sum(np.abs(np.array(list_real) - np.array(list_expected)))
    prev_w2 = data[p_prev]["weights"][action]["w2"]
    if error == 0:
        data[p_prev]["weights"][action]["w2"] = round(prev_w2 + 0.5, 2)
    elif prev_w2 > 0.1:
        data[p_prev]["weights"][action]["w2"] = round(prev_w2 - 0.5, 2)

    return data, data[p_prev]["weights"][action]["w2"]+data[p_prev]["weights"][action]["w1"]