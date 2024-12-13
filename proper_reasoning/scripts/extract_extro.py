import json
import os
import random
import numpy as np

# Define extroversion actions and dictionaries
extro_actions = [
    "say_an_enthusiastic_sentence",
    "say_something_funny",
    "ask_a_question",
    "say_something_to_capture_the_attention",
    "say_something_to_init_a_conversation",
    "tell_a_personal_story"
]

zzz_e={"say_an_enthusiastic_sentence":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     "say_something_funny":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "ask_a_question":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_something_to_init_a_conversation":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "tell_a_personal_story":{"w1":4,"w2":4,"expected_outcome":[1,1,1]},
     "say_something_to_capture_the_attention":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     }

zzo_e={"say_an_enthusiastic_sentence":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     "say_something_funny":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "ask_a_question":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     "say_something_to_init_a_conversation":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "tell_a_personal_story":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "say_something_to_capture_the_attention":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     }

zoz_e={"say_an_enthusiastic_sentence":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "say_something_funny":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "ask_a_question":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_something_to_init_a_conversation":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "tell_a_personal_story":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
      "say_something_to_capture_the_attention":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     }

zoo_e={"say_an_enthusiastic_sentence":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_something_funny":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     "ask_a_question":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "say_something_to_init_a_conversation":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "tell_a_personal_story":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
      "say_something_to_capture_the_attention":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     }

ozz_e={"say_an_enthusiastic_sentence":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     "say_something_funny":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "ask_a_question":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_something_to_init_a_conversation":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "tell_a_personal_story":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_something_to_capture_the_attention":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     }

ozo_e={"say_an_enthusiastic_sentence":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     "say_something_funny":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "ask_a_question":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     "say_something_to_init_a_conversation":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "tell_a_personal_story":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
      "say_something_to_capture_the_attention":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     }

ooz_e={"say_an_enthusiastic_sentence":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "say_something_funny":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "ask_a_question":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_something_to_init_a_conversation":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "tell_a_personal_story":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
      "say_something_to_capture_the_attention":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     }

ooo_e={"say_an_enthusiastic_sentence":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_something_funny":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     "ask_a_question":{"w1":4,"w2":1,"expected_outcome":[1,1,1]},
     "say_something_to_init_a_conversation":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "tell_a_personal_story":{"w1":6,"w2":2,"expected_outcome":[1,1,1]},
     "say_something_to_capture_the_attention":{"w1":0,"w2":0,"expected_outcome":[1,1,1]},
     }


default_extroversion_dict={
    "NA_N":{"weights":zzz_e,"num":[0,0,0]},
    "NA_S":{"weights":zzo_e,"num":[0,0,1]},
    "NA_A":{"weights":zoz_e,"num":[0,1,0]},
    "NA_H":{"weights":zoo_e,"num":[0,1,1]},
    "A_N":{"weights":ozz_e,"num":[1,0,0]},
    "A_S":{"weights":ozo_e,"num":[1,0,1]},
    "A_A":{"weights":ooz_e,"num":[1,1,0]},
    "A_H":{"weights":ooo_e,"num":[1,1,1]},
}

def initialize_or_load_person(person_id):
    directory = f"/home/alice/EpisodicMemory/{person_id}/"
    filename = os.path.join(directory, f"{person_id}.json")

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory
        print(f"Created directory: {directory}")
    
    # Initialize the JSON file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_extroversion_dict, f, indent=4)
        print(f"Initialized data for {person_id}.")
    
    # Load and return the data from the file
    with open(filename, "r") as f:
        return json.load(f)
    

def save_person_data(person_id, data):
    directory = f"/home/alice/EpisodicMemory/{person_id}/"
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
def choose_action_e(data, perception):
    weights = data[perception]["weights"]
    w = []
    for action in extro_actions:
        weight = weights[action]["w1"] + weights[action]["w2"]
        w.append(float(weight))
    norm = [i / sum(w) for i in w] if sum(w) != 0 else [1 / len(w)] * len(w)
    chosen_action = np.random.choice(extro_actions, p=norm)
    return chosen_action, weights[chosen_action]["w1"] + weights[chosen_action]["w2"]


# Update weights based on perception change
def update_weights_e(data, action, p_prev, p_after):
    list_real = data[p_after]["num"]
    list_expected = data[p_prev]["weights"][action]["expected_outcome"]
    error = sum(np.abs(np.array(list_real) - np.array(list_expected))) / len(list_real)
    prev_w2 = data[p_prev]["weights"][action]["w2"]

    if error == 0:
        data[p_prev]["weights"][action]["w2"] = round(prev_w2 + 0.5, 2)
    elif prev_w2 > 0.1:
        data[p_prev]["weights"][action]["w2"] = round(prev_w2 - 0.5, 2)

    return data, data[p_prev]["weights"][action]["w2"]+data[p_prev]["weights"][action]["w1"]
        

        