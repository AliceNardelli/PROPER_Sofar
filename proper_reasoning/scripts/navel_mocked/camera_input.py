#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import asyncio
from flask import Flask, request, jsonify
import time
import random
import requests

headers = {'Content-Type': 'application/json'}
size_window = 10
app = Flask(__name__)

data = {
    "new_perception": "",
    "emotion": "",
    "attention": "",
}

actual_emotion = ""
perception_to_take = False
gaze = ""
emotion_dict_interface = {'anger': "A", 'happy': "H", 'neutral': "N", 'sad': "SA", 'surprise': "SU"}

url_emoACT = 'http://10.186.13.9:4000/'

@app.route('/get_camera_input', methods=['PUT'])
def get_cam_input():
    global perception_to_take, actual_emotion, gaze
    updated_data = request.get_json()
    data.update(updated_data)
    if perception_to_take:
        perception_to_take = False
        data["new_perception"] = "True"
        data["emotion"] = emotion_dict_interface[actual_emotion]
        data["attention"] = gaze
    else:
        data["new_perception"] = "False"
    print("Sent data")
    return jsonify(data)


async def perception():
    global actual_emotion, gaze, perception_to_take
    while True:
        await asyncio.sleep(2)  # Fix: Use 'await' here
        random_number = random.choice([0, 1])
        if random_number == 0:
            perception_to_take = True
            gaze = "positive" if random.choice([True, False]) else "negative"
            actual_emotion = random.choice(['anger', 'happy', 'neutral', 'sad', 'surprise'])
            payload = {"emotion": emotion_dict_interface[actual_emotion], "attention": gaze}
            try:
                resp = requests.post(url_emoACT + 'navel_perception', json=payload, headers=headers)
                print(gaze, actual_emotion)
            except requests.exceptions.RequestException as e:
                print(f"Failed to connect to external service: {e}")


async def run_flask_app():
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:5019"]
    await serve(app, config)


async def main():
    await asyncio.gather(run_flask_app(), perception())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
