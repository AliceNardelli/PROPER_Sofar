#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import asyncio
from flask import Flask, request, jsonify
import navel
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig

app = Flask(__name__)

data = {
    "new_sentence": "",
    "sentence": "",
}

n_s = False
user_speech = ""

@app.route('/get_mic_input', methods=['PUT'])
def get_m_input():
    global user_speech, n_s
    updated_data = request.get_json()
    data.update(updated_data)
    if n_s:
        data["new_sentence"] = "True"
        data["sentence"] = user_speech
        n_s = False
    else:
        data["new_sentence"] = "False"
    return jsonify(data)

async def chat():
    # Load variables
    language = "it-IT"

    speech_key = "c6986565293c45098cb640f879d80254"  # Replace with your actual Azure Speech key
    speech_region = "westeurope"

    # Set up Azure Speech Config
    audio_config = AudioConfig(use_default_microphone=True)
    speech_config = SpeechConfig(
        subscription=speech_key,
        region=speech_region,
        speech_recognition_language=language,
    )

    async with navel.Robot() as robot:
        global user_speech, n_s
        while True:
            user_speech = await get_user_speech(speech_config, audio_config)

            if not user_speech:
                continue

            print(f"User said: {user_speech}")
            n_s = True

async def get_user_speech(speech_config: SpeechConfig, audio_config: AudioConfig):
    """Run recognize_once in a thread so it can be cancelled if needed.
    Uses a new recognizer every time to avoid listening to old data."""
    speech_recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Listening...")
    loop = asyncio.get_event_loop()
    res = await loop.run_in_executor(None, speech_recognizer.recognize_once)
    
    return res.text

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
