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

HOST = '172.30.64.1'
PORT = '2001'
URL_SERVER_SESSION = f'http://{HOST}:{PORT}/api/'


API_POST_ACTION = URL_SERVER_SESSION + 'post_action'


class ClientProper:

    def post_action(self, action, agent_emotion, language_style, gaze_behavior):
        payload = {
            'action':  action,
            'emotion': agent_emotion,
            'language_style': language_style,
            'gaze_behavior': gaze_behavior
        }
        requests.post(API_POST_ACTION, json=payload, timeout=5)

    
    
    
        