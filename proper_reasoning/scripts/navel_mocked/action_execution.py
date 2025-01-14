#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from flask import Flask, request, jsonify
import asyncio
import time
import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound

app = Flask(__name__)

data = {
    "":"",
}

url='http://127.0.0.1:5020/'
headers= {'Content-Type':'application/json'}

data_a ={
    "activate":"False"
}              


def reproduce_sentence(sentence):
    print(f"Reproducing sentence: '{sentence}'")
    tts = gTTS(text=sentence, lang='it')
    tts.save("output.mp3")
    playsound("output.mp3")
    os.remove("output.mp3")               
            

@app.route('/exec_actions', methods=['PUT'])
def exec():
    updated_data = request.get_json()
    data.update(updated_data)
    data_a["activate"]="False"
    res =requests.put(url+'activate_recognizer', json=data_a, headers=headers)
    reproduce_sentence(data["sentence"])
    data_a["activate"]="True"
    requests.put(url+'activate_recognizer', json=data_a, headers=headers)
    time.sleep(3)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5022, debug=True)