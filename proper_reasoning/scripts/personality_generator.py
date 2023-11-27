#!/usr/bin/env python
import os
import shutil
import subprocess
import json
import time
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np
import rospy

model = AutoModelForSequenceClassification.from_pretrained("/home/alice/personality_generator_model_new", num_labels=21, problem_type="multi_label_classification") 
tokenizer=AutoTokenizer.from_pretrained("/home/alice/prams_model", problem_type="multi_label_classification")

def generate_params(personality, action):
    text = personality + tokenizer.sep_token + action
    encoding = tokenizer(text, return_tensors="pt")
    encoding = {k: v.to("cpu") for k,v in encoding.items()}
    outputs = model(**encoding)
    logits = outputs.logits
    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(logits.squeeze().cpu())
    predictions = np.zeros(probs.shape)
    predictions[np.where(probs >= 0.5)] = 1
    params=list(predictions)
    
    return params




