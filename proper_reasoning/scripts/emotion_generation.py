import os
import json
import openai
import ast
from omegaconf import OmegaConf
from openai import OpenAI

#openai vars
file_path_openai_config = "/home/alice/PROPER_Sofar/proper_reasoning/resources/config_openai_EI.yaml"
openai_config = OmegaConf.load(file_path_openai_config).config
openai.organization = "org-OWePijhLCGVSJWhT7TQXBK7D"
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
system_message_dict = {"Agreeable":openai_config.system_message_A,
                       "Disgreeable":openai_config.system_message_E,
                       "Extrovert":openai_config.system_message_E,
                       "Introvert":openai_config.system_message_I,
                       "Conscientious":openai_config.system_message_C,
                       "Unscrupolous":openai_config.system_message_U,
                       }

model="gpt-4o"

map_emotion={
   "SA":"Sad",
   "SU":"Happy",
   "H":"Happy",
   "A":"Angry",
   "D":"Angry",
   "F":"Angry",
   "N":"Neutral",
   "":"",
}

def generate_emotion( text, user_emotion, comfortability, personality):
    user_input = "{"
    if text != None:
        user_input = "text:"
        user_input += text
        user_input += ", "
    user_input += ", user_emotion: "
    user_input += map_emotion[user_emotion]
    user_input += ", comfortability: "
    user_input += comfortability

    user_input += "}"
    print(f'This is the user input to the LLM:{user_input}')
    messages = [
        {"role": "system", "content": system_message_dict[personality]},
    ]
    # Add each new message to the list
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        top_p=1,
    )

    res = json.loads(response.choices[0].message.content)
    return res["robot_emotion"]