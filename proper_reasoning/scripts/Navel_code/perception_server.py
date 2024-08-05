#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

data = {
    'sentence':"",
}

data_mic = {
    "new_sentence":"",
    "sentence": "",
}

url='http://127.0.0.1:5020/'
url2='http://127.0.0.1:5019/'
headers= {'Content-Type':'application/json'}

@app.route('/get_input', methods=['PUT'])
def get_input():
    updated_data = request.get_json()
    data.update(updated_data)
    print("Received new input:", updated_data)
    
    try:
        
        # Fetch from get_mic_input on port 5020
        mic_response =requests.put(url+'get_mic_input', json=data_mic, headers=headers)
        data['sentence'] = eval(mic_response.text)["sentence"]
        data['new_sentence'] = eval(mic_response.text)["new_sentence"]
        
        # Fetch from get_camera_input on port 5019
        camera_response = requests.put(url2+'get_camera_input', json=data, headers=headers)
        
        data['emotion'] = eval(camera_response.text)["emotion"]
        data['new_emotion'] = eval(camera_response.text)["new_perception"]
        data['attention'] = eval(camera_response.text)["attention"]
        data['new_attention'] = eval(camera_response.text)["new_perception"]
        print(data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5021, debug=True)