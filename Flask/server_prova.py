from flask import Flask, request, jsonify
import os
import shutil
import subprocess
import json
import time
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np


data = {
    "name": "Plan",
}

data_action = {
    "action": "Plan",
}

data_params = {
    "param": "Plan",
}

model = AutoModelForSequenceClassification.from_pretrained("/home/alice/prams_model", num_labels=21, problem_type="multi_label_classification") 
tokenizer=AutoTokenizer.from_pretrained("/home/alice/prams_model", problem_type="multi_label_classification")
app = Flask(__name__)


@app.route ('/parameters', methods = ['PUT'] )

def get_params():
    # Get the updated data from the request
    updated_data = request.get_json()
    data_action.update(updated_data)
    
    text = data_action["personality"] + tokenizer.sep_token + data_action["action"]
    print(text)
    encoding = tokenizer(text, return_tensors="pt")
    encoding = {k: v.to("cpu") for k,v in encoding.items()}
    outputs = model(**encoding)
    logits = outputs.logits
    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(logits.squeeze().cpu())
    predictions = np.zeros(probs.shape)
    predictions[np.where(probs >= 0.5)] = 1
    print(list(predictions))
    data_params["param"]=list(predictions)
    return jsonify(data_params)


@app.route ('/planner_launch', methods = ['PUT'] )

def update_data():
    # Get the updated data from the request
    updated_data = request.get_json()
    print(updated_data)
    # Update the existing data with the updated data
    data.update(updated_data)
    planner_path = "/home/alice/PROPER_Sofar/downward/"
    os.chdir (planner_path)
    #shutil.copyfile(mydir+'/domain.pddl', planner_path+"/domain.pddl")
    #shutil.copyfile(mydir+'/problem.pddl', planner_path+"/problem.pddl")
    print ('./fast-downward.py task_domain.pddl problem.pddl --evaluator "h=ff()" --search "lazy_greedy([h], preferred=[h])"')
    command =  './fast-downward.py task_domain.pddl problem.pddl --evaluator "h=ff()" --search "eager_wastar([h], preferred=[h], reopen_closed=false)"'
    #run the planner
    fd_process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = fd_process.communicate()
    fd_exit = fd_process.returncode
    if os.path.isfile(planner_path+'/sas_plan'):
        print ('il piano ce')
        output_path=planner_path+'/sas_plan'
        with open(output_path, "r") as plan_file:
            raw_plan = plan_file.readlines()
        
        plan=[]
        for p in raw_plan:
           plan.append(p)
           print(p)        
        my_plan= str(raw_plan)
        
        Plan={"plan": plan,}
             
    else:
        print("Plan not found")
    # Return the updated data as a JSON response
    return jsonify(Plan)

    
if __name__=='__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
