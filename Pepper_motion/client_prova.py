import requests
from collections import OrderedDict
import numpy as np

traits=["Introvert","Extrovert","Conscientious","Unscrupulous","Agreeable","Disagreeable"]
weights=[0.5,0.0,0.0,0.5,0.0,0.0] 
objects=["l1","l2","l3"]
url='http://127.0.0.1:5008/'
headers= {'Content-Type':'application/json'}
dict = {
    'action': "Plan",
    "personality":"p",
}
pitch={"no_active":[0,0],
       "low":[0,1],
       "mid":[1,0],
       "high":[1,1],
       }
rev_pitch={str(v) : k for k,v in pitch.items()}
volume={
    "no_active":[0,0,0],
    "low":[0,0,1],
    "mid":[0,1,0],
    "dynamic":[0,1,1],
    "very_dynamic":[1,0,0],
}
rev_volume={str(v) : k for k,v in volume.items()}
velocity={"no_active":[0,0,0],
       "low":[0,0,1],
       "mid":[0,1,0],
       "rather_high":[0,1,1],
       "high":[1,0,0],
       }
rev_velocity={str(v) : k for k,v in velocity.items()}
gaze={
    "no_active":[0,0],
    "avoid": [0,1],
    "mutual":[1,0]
}
rev_gaze={str(v) : k for k,v in gaze.items()}
head={
    "no_active":[0,0,0],
    "tilt_down_shaking":[0,0,1],
    "tilt_up_shaking":[0,1,0],
    "nodding":[0,1,1],
    "shaking_low":[1,0,0],
    "shaking":[1,1,1],   
}
rev_head={str(v) : k for k,v in head.items()}
amplitude={
    "no_active":[0,0],
    "low":[0,1],
    "mid":[1,0],
    "high":[1,1],
}

rev_amplitude={str(v) : k for k,v in amplitude.items()}
g_speed={
    "no_active":[0,0],
    "low":[0,1],
    "mid":[1,0],
    "high":[1,1],
}

rev_g_speed={str(v) : k for k,v in g_speed.items()}
prox={    
    "no_active":[0,0],
    "near":[0,1],
    "mid":[1,0],
    "far":[1,1],
}
rev_prox={str(v) : k for k,v in prox.items()}
speed={    
    "no_active":[0,0],
    "low":[0,1],
    "mid":[1,0],
    "high":[1,1],
}
rev_speed={str(v) : k for k,v in speed.items()}

reversed={
    "pitch": rev_pitch,
    "volume": rev_volume,
    "velocity":rev_velocity,
    "gaze": rev_gaze,
    "head":rev_head,
    "amplitude":rev_amplitude,
    "g_speed":rev_g_speed,
    "speed":rev_speed,
    "prox":rev_prox
}
bit_map=[2,3,3,2,3,2,2,2,2]
parameters=["pitch","volume","velocity","gaze","head","amplitude","g_speed","speed", "prox"]

def get_map(predictions):
    c=0
    result={p:[] for p in parameters}
    
    for i in range(len(bit_map)):
        param=parameters[i]
        no_bit=bit_map[i]
        bits=predictions[c:c+no_bit]
        c+=no_bit
        value=reversed[param][str(list([int(b) for b in bits]))]
        #print(param,bits,value)
        result[param]=value
    
    return result

def extract_personality():
  return np.random.choice(traits,p=weights)

def server_interface():
    response_put= requests.put(url+'planner_launch', json=dict, headers=headers)   
    my_plan = response_put.text
    plan=eval(my_plan)["plan"]
    cost=plan.pop()
    return plan,cost
        
def get_params(action):
    for o in objects:
        action=action.replace(o,"")
    dict["action"]=action
    personality=extract_personality()
    dict["personality"]=personality
    resp=requests.put(url+'parameters', json=dict, headers=headers)
    m=get_map(eval(resp.text)["param"])   
    return eval(resp.text)["param"], m, personality
    

