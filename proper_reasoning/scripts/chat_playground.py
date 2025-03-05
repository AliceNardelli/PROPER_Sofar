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


traits_des={"Extrovert":openai_config.system_message_describe_e,
            "Introvert": openai_config.system_message_describe_i,
            "Conscientious": openai_config.system_message_describe_c,
            "Unscrupolous": openai_config.system_message_describe_u,
            "Agreeable": openai_config.system_message_describe_a,
            "Disagreeable": openai_config.system_message_describe_d}



messages_hint=[]
openai_config_hint = OmegaConf.load(file_path_openai_config_dict["hint"]).config
actual_quiz="quiz1"


def generate_sentence(p1, s1, ls1, p2, s2, ls2, action, user_emotion, robot_emotion, text):


    system_message_updated=system_message.replace(
        "{TRAIT1}", p1
    ).replace(
        "{TRAIT1_LEVEL}", str(s1)
    ).replace(
        "{L_S1}", ls1
    ).replace(
        "{TRAIT1_DESCRIPTION}", traits_des[p1]
    ).replace(
        "{TRAIT2}", p2
    ).replace(
        "{TRAIT2_LEVEL}", str(s2)
    ).replace(
        "{L_S2}", ls2
    ).replace(
        "{TRAIT2_DESCRIPTION}", traits_des[p2]
    ).replace(
        "{ACTION}",
        action
    ).replace(
        "{TEXT}",
        text
    ).replace(
        "{U_E}",
        user_emotion
    ).replace(
        "{R_E}",
        robot_emotion
    )


    print(system_message_updated)
    start_message = [
            {"role": "system", "content": system_message_updated},
        ]

 

    response = client.chat.completions.create(
        model=model,
        messages=start_message,
        temperature=1,
        top_p=1,
    )

    print(response.choices[0].message.content)
    #chat_message = emoji.replace_emoji(string=chat_message, replace='')
    try:
        res = json.loads(response.choices[0].message.content)
    except:
        return "", "chat"
    return res["text"], "chat"

def generate_sentenceold(user_emotion, robot_emotion, text, personality, response_style, action):
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
    return res["text"], "chat"


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
        system_message2 = openai_config_hint.system_message_quiz2.replace("XX", solution[0:2]).replace("XY", sentence).replace("XZ", solution)

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
        try:
            # Parse the JSON response for the hint
            res = json.loads(chat_message)

            # Append the hint to the history of messages
            messages_hint.append({"role": "user", "content": res["hint"]})
            print("GENERATED HINT ", res["hint"])
            print("---------------------------------")
            # Return the hint
            return res["hint"]
        except:
            return ""
    except json.JSONDecodeError as e:
        print("Failed to decode the JSON response:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

