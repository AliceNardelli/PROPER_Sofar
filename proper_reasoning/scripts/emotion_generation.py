import os
import json
import openai
import ast
from omegaconf import OmegaConf


#openai vars
file_path_openai_config = "/home/alice/PROPER_Sofar/proper_reasoning/resources/config_openai_personality_v2_it.yaml"
openai_config = OmegaConf.load(file_path_openai_config).config
openai.organization = "org-OWePijhLCGVSJWhT7TQXBK7D"
openai.api_key = os.getenv("OPENAI_API_KEY")

system_message_dict = {"Agreeable":openai_config.system_message_A,
                       "Disgreeable":openai_config.system_message_E,
                       "Extrovert":openai_config.system_message_E,
                       "Introvert":openai_config.system_message_I,
                       "Conscientious":openai_config.system_message_C,
                       "Unscrupolous":openai_config.system_message_U,
                       }


def generate_emotion( text, user_emotion, comfortability, personality):
    user_input = "{"
    if text != None:
        user_input = "text:"
        user_input += text
        user_input += ", "
    user_input += ", user_emotion: "
    user_input += user_emotion
    user_input += ", comfortability: "
    user_input += comfortability

    user_input += "}"
    print(f'This is the user input to the LLM:{user_input}')
    messages = [
        {"role": "system", "content": system_message_dict[personality]},
    ]
    # Add each new message to the list
    messages.append({"role": "user", "content": user_input})

    # Request gpt-3.5-turbo for chat completion
    response = openai.ChatCompletion.create(
        model="gpt-4i",
        messages=messages, 
        #max_tokens=max_tokens
        
    )

    res = json.loads(response.choices[0].message.content)
    return res["emotion"]