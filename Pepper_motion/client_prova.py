import requests
from collections import OrderedDict
import numpy as np

traits=["Introvert","Extrovert","Conscientious","Unscrupulous","Agreeable","Disagreeable"]
weights=[0.3,0.0,0.0,0.3,0.4,0.0]
objects=["l1","l2","l3"]
url='http://127.0.0.1:5008/'
headers= {'Content-Type':'application/json'}
dict = {
    'action': "Plan",
    "personality":"p",
}

def extract_personality():
  return np.random.choice(traits,p=weights)

def server_interface():
    response_put= requests.put(url+'planner_launch', json=dict, headers=headers)   
    my_plan = response_put.text
    plan=eval(my_plan)["plan"]
    cost=plan.pop()
    return plan,cost
        


def get_params(p):
    action=p.replace("\n","").replace("(","").replace(")","").replace("_"," ").replace('"','')
    for o in objects:
        action=action.replace(o,"")
    dict["action"]=action
    print(action)
    personality=extract_personality()
    dict["personality"]=personality
    resp=requests.put(url+'parameters', json=dict, headers=headers)
    return eval(resp.text)["param"]
    

