#!/usr/bin/env python
# -*- coding: utf-8 -*-

from get_parameters import *
from personality_generator import *
import requests
from emotion_generation import *
from chat_playground import *
from omegaconf import OmegaConf

url='http://10.186.13.34:5022/'
url_emoACT='http://10.186.13.9:3000/emotional_state'
url_emoACT2='http://10.186.13.9:8008/'

headers= {'Content-Type':'application/json'}
expression=""
data_action={
        "facial_expression":"",
        "sentence":"",
        "volume":"",
        "gaze":"",
        "tone":"",
        "g_amplitude":"",
        "head":""       
}

traits_res=["Extrovert","Introvert","Conscientious","Unscrupolous","Agreeable","Disagreeable"]

emotion_label_map={
        "H":"Happy",
        "A":"Angry",
        "F":"Fear",
        "SA":"Sad",
        "SU":"Surprised",
        "D":"Disgusted",
        "N":"Neutral"
}

def dispatch_action(action, personality, user_emotion, user_sentence, comfortability, weights_res, quiz, solution, sentence, to_say_sentence, number):
        payload = {"comfortability": comfortability}
        response = requests.post(url_emoACT2+'comfortability', json=payload, headers=headers)
        #takes parameters
        params=generate_params(personality, action)
        mmap =get_map(params,personality)
        personality_sentence=""
        language_sentence=""
        for i in range(len(weights_res)):
                if weights_res[i]!=0:
                        personality_sentence=personality_sentence+" "+traits_res[i]
                        if traits_res[i]==personality:
                                language_sentence=language_sentence+" "+mmap["language"]
                        else:
                                params_l=generate_params(traits_res[i], action)
                                mmap_l =get_map(params_l,traits_res[i])
                                language_sentence=language_sentence+" "+mmap_l["language"]
        print("PERSONALITY and LANGUAGE paramos: "+ personality_sentence+" "+language_sentence)

        
        print("generate the current robot emotion ********************")
        try:
                response = requests.get(url_emoACT)
                if response.status_code == 200:
                        data = response.json()  # Parse the JSON response
                        robot_emotion = emotion_label_map[data.get("emotion_label")]
                        new_emotion = data.get("new_emotion")
                        epa = data.get("emotion")
                        expression=epa[0]
                        print(f"Emotion: {robot_emotion}")
                else:
                        print(f"Failed to retrieve emotion. Status code: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

        #TO DO: send the comfortability
        if ("REACT" not in action) and ("WAIT" not in action) and ("NOT_ANSWER" not in action) and ("CHECK" not in action):
                action=action.replace("_"," ").lower()
                
                if (action == "say sentence"):
                        robot_sentence = to_say_sentence
                        tone="chat"

                elif (action == "say number"):
                        robot_sentence = str(number)
                        tone="chat"
                elif (action=="present escape room"):
                        sentence_to_say = OmegaConf.load("/home/alice/PROPER_Sofar/proper_reasoning/resources/quiz.yaml").presentation
                        action_to_fullfill= "say: '"+sentence_to_say+"'"
                        robot_sentence, tone = generate_sentence(user_emotion, robot_emotion, "", personality_sentence, language_sentence, action_to_fullfill)

                elif (action=="present quiz"):
                        if quiz=="quiz1":
                                sentence_to_say = OmegaConf.load("/home/alice/PROPER_Sofar/proper_reasoning/resources/quiz.yaml").present_quiz1
                        elif quiz=="quiz2":
                                sentence_to_say = OmegaConf.load("/home/alice/PROPER_Sofar/proper_reasoning/resources/quiz.yaml").present_quiz2_1+sentence+OmegaConf.load("/home/alice/PROPER_Sofar/proper_reasoning/resources/quiz.yaml").present_quiz2_2

                        else:
                                sentence_to_say = OmegaConf.load("/home/alice/PROPER_Sofar/proper_reasoning/resources/quiz.yaml").present_quiz3

                        action_to_fullfill= "say: '"+sentence_to_say+"'"
                        robot_sentence, tone = generate_sentence(user_emotion, robot_emotion, "", personality_sentence, language_sentence, action_to_fullfill)

                elif (action=="guess quiz"):
                        if quiz=="quiz1":
                                sentence_to_say = OmegaConf.load("/home/alice/PROPER_Sofar/proper_reasoning/resources/quiz.yaml").guess_quiz1
                        elif quiz=="quiz2":
                                sentence_to_say = OmegaConf.load("/home/alice/PROPER_Sofar/proper_reasoning/resources/quiz.yaml").guess_quiz2
                        else:
                                sentence_to_say = OmegaConf.load("/home/alice/PROPER_Sofar/proper_reasoning/resources/quiz.yaml").guess_quiz3
                                
                        action_to_fullfill= "say: '"+sentence_to_say+"'"
                        robot_sentence, tone = generate_sentence(user_emotion, robot_emotion, "", personality_sentence, language_sentence, action_to_fullfill)
                elif (action=="give hint"):
                        if quiz=="quiz3":
                                robot_sentence = to_say_sentence
                                tone="chat"   
                        else:
                                generated_hint=generate_hint(quiz,solution, sentence)
                                action_to_fullfill= "say: '"+generated_hint+"'"
                                robot_sentence, tone = generate_sentence(user_emotion, robot_emotion, "", personality_sentence, language_sentence, action_to_fullfill)
                                print(" HINT: ")
                                print(generated_hint)
                else:
                        robot_sentence, tone = generate_sentence(user_emotion, robot_emotion, user_sentence, personality_sentence, language_sentence, action)
                
                print(robot_sentence)

                data_action["facial_expression"]=robot_emotion
                data_action["sentence"]=robot_sentence
                data_action["volume"]=mmap["volume"]
                data_action["gaze"]=mmap["gaze"]
                data_action["tone"]=tone
                if "Extrovert" in personality_sentence:
                        data_action["g_amplitude"]="high"
                elif "Introvert" in personality_sentence:
                        data_action["g_amplitude"]="low"
                else:
                        data_action["g_amplitude"]=mmap["amplitude"]
                data_action["head"]=mmap["head"]
                print(data_action)
                resp=requests.put(url+'exec_actions', json=data_action, headers=headers)
                time.sleep(2)
                return True, action, expression
        return True, action, 101
        
    





        
