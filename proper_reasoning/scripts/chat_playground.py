import os
import openai
from openai import OpenAI
from omegaconf import OmegaConf
#import emoji
import json

from flask import Flask, request, jsonify

#openai vars
file_path_openai_config = "/home/alice/PROPER_Sofar/proper_reasoning/resources/config_openai_personality_v2_it.yaml"
openai_config = OmegaConf.load(file_path_openai_config).config
openai.organization = "org-OWePijhLCGVSJWhT7TQXBK7D"
openai.api_key = os.getenv("OPENAI_API_KEY")
system_message = openai_config.system_message
# Create a list to store all the messages for context
start_message = [
    {"role": "system", "content": system_message},
]
model="gpt-4i"

client = OpenAI()



def generate_sentence(user_emotion, robot_emotion, text, personality, response_style, action):
   
    updated_data = request.get_json()
    
    
    user_input = "{"
    user_input += "text: "
    user_input += text
    user_input += ", user_emotion: "
    user_input += user_emotion
    user_input += ", robot_emotion: "
    user_input += robot_emotion
    user_input += ", personality: "
    user_input += personality
    user_input += ", response_style: "
    user_input += response_style
    user_input += ", action: "
    user_input += action
    

    user_input += "}"
    print(user_input)
    # Add each new message to the list
    messages=start_message
    messages.append({"role": "user", "content": user_input})
   

    response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=1,
    top_p=1,
    )

    # Print the response and add it to the messages list
   
    
    print(response.choices[0].message.content)
    #chat_message = emoji.replace_emoji(string=chat_message, replace='')
    res = json.loads(response.choices[0].message.content)
    return res["text"], res["voice_style"]


