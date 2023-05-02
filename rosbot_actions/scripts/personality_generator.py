
import os
import shutil
import subprocess
import json
import time
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np

model = AutoModelForSequenceClassification.from_pretrained("/home/alice/prams_model", num_labels=21, problem_type="multi_label_classification") 
tokenizer=AutoTokenizer.from_pretrained("/home/alice/prams_model", problem_type="multi_label_classification")

text = "Extrovert" + tokenizer.sep_token + "move"
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

  

