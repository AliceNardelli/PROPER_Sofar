import os
import openai
from openai import OpenAI
from omegaconf import OmegaConf
#import emoji
import json

from flask import Flask, request, jsonify

#openai vars
file_path_openai_config_dict = {"Agreeable":"/home/alice/PROPER_Sofar/proper_reasoning/resources/config_openai_A.yaml",
                       "Disagreeable":"/home/alice/PROPER_Sofar/proper_reasoning/resources/config_openai_D.yaml",
                       "Extrovert":"/home/alice/PROPER_Sofar/proper_reasoning/resources/config_openai_E.yaml",
                       "Introvert":"/home/alice/PROPER_Sofar/proper_reasoning/resources/config_openai_I.yaml",
                       "Conscientious":"/home/alice/PROPER_Sofar/proper_reasoning/resources/config_openai_C.yaml",
                       "Unscrupolous":"/home/alice/PROPER_Sofar/proper_reasoning/resources/config_openai_U.yaml",
                       "global":"/home/alice/PROPER_Sofar/proper_reasoning/resources/config_openai_personality_v2_it.yaml",
                       }

openai.organization = "org-OWePijhLCGVSJWhT7TQXBK7D"
openai.api_key = os.getenv("OPENAI_API_KEY")

model="gpt-4o"

client = OpenAI()

map_emotion={
   "SA":"Sad",
   "SU":"Happy",
   "H":"Happy",
   "A":"Angry",
   "D":"Angry",
   "F":"Angry",
   "N":"Neutral",
}
messages={}

def generate_sentence(user_emotion, robot_emotion, text, personality, response_style, action):
    openai_config = OmegaConf.load(file_path_openai_config_dict["global"]).config
    system_message = openai_config.system_message
    start_message = [
        {"role": "system", "content": system_message},
    ]
    user_input = "{"
    user_input += "text: "
    user_input += text
    user_input += ", user_emotion: "
    user_input += map_emotion[user_emotion]
    user_input += ", robot_emotion: "
    user_input += robot_emotion
    user_input += ", personality: "
    user_input += personality
    user_input += ", response_style: "
    user_input += response_style
    user_input += ", action: "
    user_input += action
    

    user_input += "}"
    # Add each new message to the list
    new_message=start_message
    messages.append({"role": "user", "content": user_input})
    new_message.append({"role": "user", "content": messages})
    print(messages)
    print(new_message)

    response = client.chat.completions.create(
        model=model,
        messages=new_message,
        temperature=1,
        top_p=1,
    )

    print(response.choices[0].message.content)
    #chat_message = emoji.replace_emoji(string=chat_message, replace='')
    res = json.loads(response.choices[0].message.content)
    return res["text"], res["voice_style"]


