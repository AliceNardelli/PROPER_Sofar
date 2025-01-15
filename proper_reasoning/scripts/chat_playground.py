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
                       "hint":"/home/alice/PROPER_Sofar/proper_reasoning/resources/generate_hint.yaml"
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

openai_config = OmegaConf.load(file_path_openai_config_dict["global"]).config
system_message = openai_config.system_message
start_message = [
        {"role": "system", "content": system_message},
    ]

messages_hint=[]
openai_config_hint = OmegaConf.load(file_path_openai_config_dict["hint"]).config
actual_quiz="quiz1"

def generate_sentence(user_emotion, robot_emotion, text, personality, response_style, action):
    
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
    
    start_message.append({"role": "user", "content": user_input})
    

    response = client.chat.completions.create(
        model=model,
        messages=start_message,
        temperature=1,
        top_p=1,
    )

    print(response.choices[0].message.content)
    #chat_message = emoji.replace_emoji(string=chat_message, replace='')
    res = json.loads(response.choices[0].message.content)
    return res["text"], res["voice_style"]


def generate_hint(quiz, solution, sentence):
    global actual_quiz, messages_hint
    print("---------------------------------")
    print("FROM CHAT PLAYGROUND")
    print("Solution: ", solution)
    # Check if this is a new quiz and reset messages if needed
    if actual_quiz != quiz:
        actual_quiz = quiz
        messages_hint = []

    # Check if it's the first hint
    if not messages_hint and quiz == "quiz1":
        # If no hints have been generated yet, return the predefined first hint
        first_hint = "Date un occhio dentro alla scatola"
        messages_hint.append({"role": "user", "content": first_hint})
        print("GENERATED HINT ", first_hint)
        print("---------------------------------")
        return first_hint

    # Select the appropriate system message based on the quiz type
    if quiz == "quiz1":
        system_message2 = openai_config_hint.system_message_quiz1.replace("XXX", solution)
    else:
        system_message2 = openai_config_hint.system_message_quiz2.replace("XX", solution).replace("XY", sentence)

    # Initialize the message list for the OpenAI API
    start_message2 = [
        {"role": "system", "content": system_message2},
    ]

    # Append the previous hints if they exist
    start_message2.extend(messages_hint)
    print("PROMPT TO LLM: ", start_message2)
    # Make the API call to OpenAI
    try:
        response = client.chat.completions.create(
            model=model,
            messages=start_message2,
            temperature=1,
            top_p=1,
        )
        # Extract the content of the response
        chat_message = response.choices[0].message.content

        # Parse the JSON response for the hint
        res = json.loads(chat_message)

        # Append the hint to the history of messages
        messages_hint.append({"role": "user", "content": res["hint"]})
        print("GENERATED HINT ", res["hint"])
        print("---------------------------------")
        # Return the hint
        return res["hint"]
    except json.JSONDecodeError as e:
        print("Failed to decode the JSON response:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

