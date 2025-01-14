#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from flask import Flask, request, jsonify
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig

app = Flask(__name__)

data = {
    "new_sentence": "",
    "sentence": "",
    "listening": "",
}

data_activate = {
    "activate": "True"
}

n_s = False
l = False
user_speech = ""
activate = 0
cancel=False

@app.route('/activate_recognizer', methods=['PUT'])
def stop():
    global user_speech, n_s, l, cancel
    updated_data = request.get_json()
    global activate
    if updated_data["activate"] == "True":
        user_speech=""
        n_s=False
        l=False
        activate = 1
        cancel=True
        print("CLEAR NAVEL SPEECH")
    else:
        activate = 2
    print("ACTIVATE CALLBACK: activate =", activate)
    return jsonify(updated_data)

@app.route('/get_mic_input', methods=['PUT'])
def get_m_input():
    global user_speech, n_s, l
    updated_data = request.get_json()
    data.update(updated_data)
    if n_s:
        data["new_sentence"] = "True"
        data["sentence"] = user_speech
        data["listening"] = "False"
        n_s = False
        l = False
    else:
        if l:
            data["listening"] = "True"
        else:
            data["listening"] = "False"
        data["new_sentence"] = "False"
    
    print(data)
    return jsonify(data)

def speech_start_detected_callback(evt):
    print("Speech start detected: {}".format(evt))

def speech_end_detected_callback(evt):
    print("Speech end detected: {}".format(evt))

def recognized_callback(evt):
    global user_speech, n_s, l, cancel
    if evt.result.text != "":
        if cancel:
            user_speech = ""
            n_s = False
            l = False
            cancel=False
        else:
            user_speech = evt.result.text
            n_s = True
            l = False
            print("Recognized: {}".format(evt.result.text))
            print(user_speech)
        

def recognizing_callback(evt):
    global l
    l = True
    print("Recognizing: {}".format(evt.result.text))

def session_started_callback(evt):
    print("Session started: {}".format(evt))

def session_stopped_callback(evt):
    print("Session stopped: {}".format(evt))

def canceled_callback(evt):
    print("Canceled: {}".format(evt))


async def chat():
    global activate
    language = "it-IT"
    print("there")
    speech_key = "8f95505a0a7f49edaa75edcf6440dcbf"  
    speech_region = "westeurope"

    # Set up Azure Speech Config
    audio_config = AudioConfig(use_default_microphone=True)
    speech_config = SpeechConfig(
        subscription=speech_key,
        region=speech_region,
        speech_recognition_language=language,
    )
    recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    # Connect the callbacks
    recognizer.recognized.connect(recognized_callback)
    recognizer.recognizing.connect(recognizing_callback)
    recognizer.session_started.connect(session_started_callback)
    recognizer.session_stopped.connect(session_stopped_callback)
    recognizer.canceled.connect(canceled_callback)
    recognizer.speech_start_detected.connect(speech_start_detected_callback)
    recognizer.speech_end_detected.connect(speech_end_detected_callback)
    print("Starting continuous recognition initially...")
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, recognizer.start_continuous_recognition)
        while True:
           
            await asyncio.sleep(0.5)

    except RuntimeError as e:
        print(f"Error starting recognizer: {e}")

    

async def run_flask_app():
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:5020"]
    await serve(app, config)

async def main():
    await asyncio.gather(
        run_flask_app(),
        chat(),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass