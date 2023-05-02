
#!/usr/bin/env python
import os
import shutil
import subprocess
import json
import time
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np
from proper_lpg.srv import PersonalityGenerator, PersonalityGeneratorResponse
import rospy

model = AutoModelForSequenceClassification.from_pretrained("/home/alice/prams_model", num_labels=21, problem_type="multi_label_classification") 
tokenizer=AutoTokenizer.from_pretrained("/home/alice/prams_model", problem_type="multi_label_classification")

def generate_params(req):
    text = req.personality + tokenizer.sep_token + req.action
    encoding = tokenizer(text, return_tensors="pt")
    encoding = {k: v.to("cpu") for k,v in encoding.items()}
    outputs = model(**encoding)
    logits = outputs.logits
    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(logits.squeeze().cpu())
    predictions = np.zeros(probs.shape)
    predictions[np.where(probs >= 0.5)] = 1
    r=PersonalityGeneratorResponse()
    r.params=list(predictions)
    return r

if __name__ == "__main__":
    rospy.init_node('personality_generatie')
    s = rospy.Service('personality_params', PersonalityGenerator, generate_params)
    print("Ready to add two ints.")
    rospy.spin()




