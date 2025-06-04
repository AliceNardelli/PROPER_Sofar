import os
import openai
from openai import OpenAI
from omegaconf import OmegaConf
#import emoji
import json

from flask import Flask, request, jsonify

#openai vars
file_path_openai_config_dict = {"prospection":"C:\\Workspace\\PROPER_Sofar\\proper_reasoning\\resources\\config_openai_prospection.yaml",
                       }

openai.organization = "org-OWePijhLCGVSJWhT7TQXBK7D"
openai.api_key = os.getenv("OPENAI_API_KEY")

model="gpt-4o"

client = OpenAI()


messages=[]
openai_config = OmegaConf.load(file_path_openai_config_dict["prospection"]).config
system_message = openai_config.system_message


def run_prospection(actual_comfortability, user_emotion, user_sentence, user_em, e_level, a_level, c_level):
    global system_message
    print(e_level)
    system_message = system_message.replace(
        "XCO", str(actual_comfortability)
    ).replace(
        "XEM", user_emotion
    ).replace(
        "XSE", user_sentence
    ).replace(
        "XLE", str(e_level)
    ).replace(
        "XLA", str(a_level)
    ).replace(
        "XLC", str(c_level)
    ).replace(
        "XUEM", user_em
    )
    
    print(system_message)
    start_message = [
        {"role": "system", "content": system_message},
    ]
    

    response = client.chat.completions.create(
        model=model,
        messages=start_message,
        temperature=1,
        top_p=1,
    )

    print(response.choices[0].message.content)
    
    res = json.loads(response.choices[0].message.content)
    return res


