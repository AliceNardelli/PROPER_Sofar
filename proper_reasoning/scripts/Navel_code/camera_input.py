#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import asyncio
from flask import Flask, request, jsonify
import navel
import time

size_window = 10
app = Flask(__name__)

data = {
    "new_perception": "",
    "emotion": "",
    "attention": "False",
}
actual_emotion = ""
window_emotion = []
perception_to_take = False
gaze = ""
emotion_dict_interface = {'anger': "A",
                          'happy': "H",
                          'neutral': "N",
                          'sad': "SA",
                          'surprise': "SU"}

emotions = ['anger', 'happy', 'neutral', 'sad', 'surprise']
emotions_intensity = [0, 0, 0, 0, 0]

@app.route('/get_camera_input', methods=['PUT'])
def get_cam_input():
    global perception_to_take, actual_emotion, gaze
    updated_data = request.get_json()
    data.update(updated_data)
    if perception_to_take:
        perception_to_take = False
        data["new_perception"] = "True"
        data["emotion"] = actual_emotion
        data["attention"] = gaze
    else:
        data["new_perception"] = "False"
    print("Sent data")
    return jsonify(data)

def is_looking_at_camera(gaze_vector, camera_position, eye_position):
    # Compute the camera vector
    camera_vector = np.array(camera_position) - np.array(eye_position)
    
    # Normalize the vectors
    gaze_vector = gaze_vector / np.linalg.norm(gaze_vector)
    camera_vector = camera_vector / np.linalg.norm(camera_vector)
    
    # Compute the dot product
    dot_product = np.dot(gaze_vector, camera_vector)
    
    # Determine if looking at camera (threshold can be adjusted)
    threshold = 0.97
    return dot_product > threshold

async def perception():
    global actual_emotion, gaze, perception_to_take
    async with navel.Robot() as robot:
        while True:
            #await asyncio.sleep(5)  # Use asyncio.sleep to avoid blocking the event loop
            data = await robot.next_frame()
            
            if data.persons:
                perception_to_take = True
                person = data.persons[0]
                print(person)
                gaze_vector = np.array([person.g_gaze[0].x, person.g_gaze[0].y, person.g_gaze[0].z])
                camera_position = np.array([0.0, 0.0, 0.0])  # Example camera position
                eye_position = np.array([person.g_eye_right[0].x, person.g_eye_right[0].y, person.g_eye_right[0].z])  # Example eye position (1 unit in front of the camera)
                is_looking = is_looking_at_camera(gaze_vector, camera_position, eye_position)
                gaze = "positive" if is_looking else "negative"
                
                emotions_intensity[0] = person.facial_expression.anger
                emotions_intensity[1] = person.facial_expression.happy
                emotions_intensity[2] = person.facial_expression.neutral
                emotions_intensity[3] = person.facial_expression.sad
                emotions_intensity[4] = person.facial_expression.surprise
                window_emotion.append(emotions[emotions_intensity.index(max(emotions_intensity))])
                
                if len(window_emotion) > size_window:
                    window_emotion.pop(0)

                actual_emotion = max(set(window_emotion), key=window_emotion.count)

async def run_flask_app():
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:5019"]
    await serve(app, config)

async def main():
    await asyncio.gather(
        run_flask_app(),
        perception(),
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
