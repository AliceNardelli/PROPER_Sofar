#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import navel
from flask import Flask, request, jsonify
import asyncio
import time
app = Flask(__name__)

data = {
    "":"",
}

url='http://127.0.0.1:5020/'
headers= {'Content-Type':'application/json'}

data_a ={
    "activate":"False"
}              

async def say(sentence, facial_expression, g_amplitude):
    
    async with navel.Robot() as robot:
            #neutral: float = 0, happy: float = 0, sad: float = 0, surprise: float = 0, anger: float = 0, smile: float = 0
            if facial_expression=="Happy":
                robot.head_facial_expression(0,1,0,0,0,0)
            if facial_expression=="Neutral":
                robot.head_facial_expression(1,0,0,0,0,0)
            if facial_expression=="Surprise":
                robot.head_facial_expression(0,0,0,1,0,0)
            if facial_expression=="Sad":
                robot.head_facial_expression(0,0,1,0,0,0)
            if facial_expression=="Angry":
                robot.head_facial_expression(0,0,0,0,1,0)
            
            robot.say(sentence)
            if facial_expression=="Happy":
                robot.head_facial_expression(0,0,0,0,0,1)
            if g_amplitude=="high":
                await robot.rotate_arms(120, 120)
                await robot.rotate_arms(0, 0)
            if g_amplitude=="middle":
                await robot.rotate_arms(100, 100)
                await robot.rotate_arms(0, 0)
            if g_amplitude=="low":
                await robot.rotate_arms(70, 70)
                await robot.rotate_arms(0, 0)

            

@app.route('/exec_actions', methods=['PUT'])
def exec():
    updated_data = request.get_json()
    data.update(updated_data)
    data_a["activate"]="False"
    res =requests.put(url+'activate_recognizer', json=data_a, headers=headers)
    asyncio.run(say("<lang,it1>"+data["sentence"], data["facial_expression"],data["g_amplitude"]))

    data_a["activate"]="True"
    requests.put(url+'activate_recognizer', json=data_a, headers=headers)
    time.sleep(3)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5022, debug=True)