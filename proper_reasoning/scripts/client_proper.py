# Copyright 2023 Reply S.p.A. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

'''
This module is used to interact with the server_session
'''

# sys modules
import time
from datetime import datetime

# external modules
import requests

HOST = '192.168.69.251'
PORT = '2001'
URL_SERVER_SESSION = f'http://{HOST}:{PORT}/api/'

API_GET_LAST_EMOTION = URL_SERVER_SESSION + 'get_last_emotion'
API_MAIN_INFO = URL_SERVER_SESSION + 'main_info'
API_PREFERRED_ACTIVITY = URL_SERVER_SESSION + 'preferred_activities'
API_USER_EMOTION = URL_SERVER_SESSION + 'user_emotion'
API_USER_ATTENTION = URL_SERVER_SESSION + 'user_attention'
API_USER_SENTENCE = URL_SERVER_SESSION + 'user_sentence'
API_USER_PRESENT = URL_SERVER_SESSION + 'user_present'
API_APPROACHING_USER = URL_SERVER_SESSION + 'approaching_user'
API_GET_INPUT = URL_SERVER_SESSION + 'get_input'
API_POST_NEW_ACTION = URL_SERVER_SESSION + 'post_new_action'
API_GET_NEW_ACTION = URL_SERVER_SESSION + 'get_new_action'
API_POST_EXEC = URL_SERVER_SESSION + 'post_exec'
API_GET_EXEC = URL_SERVER_SESSION + 'get_exec'
API_GET_SPEAKING = URL_SERVER_SESSION + 'get_speaking'
API_POST_SPEAKING = URL_SERVER_SESSION + 'set_speaking'
API_GET_PERSONALITY = URL_SERVER_SESSION + 'get_personality'
API_POST_PERSONALITY = URL_SERVER_SESSION + 'post_personality'


class ClientProper:

    def get_personality(self):
        response = requests.get(API_GET_PERSONALITY, timeout=5)
        if response.status_code == 200:
            payload = response.json()
            return payload['personality']
        else:
            print(f"Error: {response.status_code}")
            return None


    def post_personality(self, personality):
        payload = {
            'personality':  personality,
        }
        requests.post(API_POST_PERSONALITY, json=payload, timeout=5)

    def get_speaking(self):
        response = requests.get(API_GET_SPEAKING, timeout=5)
        if response.status_code == 200:
            payload = response.json()
            return payload['speaking']
        else:
            print(f"Error: {response.status_code}")
            return None


    def post_speaking(self, speaking):
        payload = {
            'stopped': speaking,
        }
        requests.post(API_POST_SPEAKING, json=payload, timeout=5)

    def save_main_info(self):
        payload = {
            'detected_main_info': True
        }
        requests.post(API_MAIN_INFO, json=payload, timeout=5)
        

    def save_preferred_activities(self):
        payload = {
            'detected_preferred_activities': True
        }
        requests.post(API_PREFERRED_ACTIVITY, json=payload, timeout=5)


    def save_emotion(self, emotion):
        payload = {
            'emotion': emotion,
            'new_emotion': True
        }
        requests.post(API_USER_EMOTION, json=payload, timeout=5)


    def save_attention(self, attention):
        payload = {
            'attention': attention,
            'new_attention': True
        }
        requests.post(API_USER_ATTENTION, json=payload, timeout=5)

    def save_sentence(self, sentence):
        payload = {
            'sentence': sentence,
            'new_sentence': True
        }
        requests.post(API_USER_SENTENCE, json=payload, timeout=5)

    def save_user_present(self, user_id):
        payload = {
            'user_id': user_id,
            'user_present': True
        }
        requests.post(API_USER_PRESENT, json=payload, timeout=5)


    def save_approaching_user(self):
        payload = {
            'approaching_user': True
        }
        requests.post(API_APPROACHING_USER, json=payload, timeout=5)


    def get_user_input(self):
        response = requests.get(API_GET_INPUT, timeout=5)
        if response.status_code == 200:
            payload = response.json()
            new_sentence = payload['new_sentence']
            new_emotion =  payload['new_emotion']
            new_attention =  payload['new_attention']
            attention = payload['attention']
            emotion = payload['emotion']
            sentence = payload['sentence']
            human_present =  payload['human_present']
            start_proactivity =  payload['start_proactivity']
            person = payload['person']
            detected_main_info=payload["detected_main_info"]
            detected_preferred_activities=payload["detected_preferred_activities"]
            return new_sentence, new_emotion, new_attention, attention, emotion, sentence, human_present, start_proactivity, person, detected_main_info, detected_preferred_activities
        
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None, None, None, None, None, None, None, None, None
    

    def get_user_last_emotion(self):
        response = requests.get(API_GET_LAST_EMOTION, timeout=5)
        if response.status_code == 200:
            payload = response.json()
            emotion = payload['emotion']
            return  emotion
        
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        
        
    def post_new_action(self,language_style, emotion,volume, gaze, action, personality):
        print("POST NEW ACTION")
        payload = {
            "language_style":language_style,
            "emotion":emotion,
            "volume":volume,
            "gaze":gaze,
            "action":action,
            "personality":personality,
            "new_action":True
        }
        requests.post(API_POST_NEW_ACTION, json=payload, timeout=5)
 
    def get_new_action(self):
        response = requests.get(API_GET_NEW_ACTION, timeout=5)
        if response.status_code == 200:
            payload = response.json()
            language_style = payload['language_style']
            emotion = payload['emotion']
            volume = payload['volume']
            action =  payload['action']
            personality =  payload['personality']
            new_action =  payload['new_action']
            gaze = payload['gaze']
            return language_style, emotion, volume, gaze , action, personality, new_action
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None, None, None, None, None, None, None
        

    def post_exec(self):
        payload = {
            "executed_action":True
        }
        requests.post(API_POST_EXEC, json=payload, timeout=5)
 
    def get_exec(self):
        response = requests.get(API_GET_EXEC, timeout=5)
        if response.status_code == 200:
            payload = response.json()
            return payload['executed_action']
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None

if __name__ == "__main__":
    client_session = ClientProper()
    client_session.post_exec()
    client_session.save_emotion("Happy")
    print(client_session.get_user_input())
    
    
        