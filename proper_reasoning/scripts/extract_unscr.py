import json
import os
import random
import numpy as np

unsc_actions=["distract_the_user_asking_a_random_question",
              "make_a_thoughtless_consideration",
              "say_something_inconsistent"]


zzz_u={"distract_the_user_asking_a_random_question":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_inconsistent":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     }

zzo_u={"distract_the_user_asking_a_random_question":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_inconsistent":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     }


zoz_u={"distract_the_user_asking_a_random_question":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_inconsistent":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     }


zoo_u={"distract_the_user_asking_a_random_question":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_inconsistent":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     }

ozz_u={"distract_the_user_asking_a_random_question":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_inconsistent":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     }

ozo_u={"distract_the_user_asking_a_random_question":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_inconsistent":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     }

ooz_u={"distract_the_user_asking_a_random_question":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_inconsistent":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     }

ooo_u={"distract_the_user_asking_a_random_question":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "make_a_thoughtless_consideration":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     "say_something_inconsistent":{"w1":8,"w2":0,"expected_outcome":[0,0,0]},
     }

default_unsc_dict={
    "NA_N":{"weights":zzz_u,"num":[0,0,0]},
    "NA_S":{"weights":zzo_u,"num":[0,0,1]},
    "NA_A":{"weights":zoz_u,"num":[0,1,0]},
    "NA_H":{"weights":zoo_u,"num":[0,1,1]},
    "A_N":{"weights":ozz_u,"num":[0,0,0]},
    "A_S":{"weights":ozo_u,"num":[0,0,1]},
    "A_A":{"weights":ooz_u,"num":[0,1,0]},
    "A_H":{"weights":ooo_u,"num":[0,1,1]},
}


def initialize_or_load_person_u(person_id):
    directory = f"/home/alice/EpisodicMemory/{person_id}/LC/"
    filename = os.path.join(directory, f"{person_id}.json")

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory
        print(f"Created directory: {directory}")
    
    # Initialize the JSON file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(default_unsc_dict, f, indent=4)
        print(f"Initialized data for {person_id}.")
    
    # Load and return the data from the file
    with open(filename, "r") as f:
        return json.load(f)
    

def save_person_data_u(person_id, data):
    directory = f"/home/alice/EpisodicMemory/{person_id}/LC/"
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
def choose_action_u(data, perception):
    weights = data[perception]["weights"]
    w = []
    for action in unsc_actions:
        weight = weights[action]["w1"] + weights[action]["w2"]
        w.append(float(weight))
    norm = [i / sum(w) for i in w] if sum(w) != 0 else [1 / len(w)] * len(w)
    chosen_action = np.random.choice(unsc_actions, p=norm)
    return chosen_action, weights[chosen_action]["w1"] + weights[chosen_action]["w2"]




