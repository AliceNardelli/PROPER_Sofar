#!/usr/bin/env python
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import shutil
import subprocess
import json
import time
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np


model = AutoModelForSequenceClassification.from_pretrained("/home/alice/Personality_Generator_Language", num_labels=11, problem_type="multi_label_classification") 
tokenizer=AutoTokenizer.from_pretrained("/home/alice/Personality_Generator_Language", problem_type="multi_label_classification")

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




