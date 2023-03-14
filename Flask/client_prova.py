import requests
from collections import OrderedDict
import numpy as np
traits=["Introvert","Extrovert","Conscientious","Unscrupulous","Agreeable","Disagreeable"]
weights=[0.3,0.0,0.0,0.3,0.4,0.0]
objects=["l1","l2","l3"]

def extract_personality():
  return np.random.choice(traits,p=weights)

def main():
    url='http://127.0.0.1:5008/'
    dict = {
        'action': "Plan",
        "personality":"p",
    }
    headers= {'Content-Type':'application/json'}
    response_put= requests.put(url+'planner_launch', json=dict, headers=headers)
    
    #print (response_put.text)
    if response_put.text == "Plan not found":
        print ('ci entro')
        
    
    else:
        my_plan = response_put.text
        plan=eval(my_plan)["plan"]
        cost=plan.pop()
        print(cost)
        for p in plan:
            action=p.replace("\n","").replace("(","").replace(")","").replace("_"," ").replace('"','')
            for o in objects:
                action=action.replace(o,"")
            dict["action"]=action
            print(action)
            personality=extract_personality()
            dict["personality"]=personality
            resp=requests.put(url+'parameters', json=dict, headers=headers)
            print(eval(resp.text)["param"])
        #print (my_plan)

   
    
if __name__ == "__main__":
    main()