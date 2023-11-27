#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
import requests
import time
url='http://127.0.0.1:5015/'
headers= {'Content-Type':'application/json'}

data={
      "new_emotion":"False",
      "new_sentence":"False",
      "emotion":""
}
emotion_dict_interface={'emotion_Angry':"A", 
                        'emotion_Disgust':"D",
                        'emotion_Fear':"F", 
                        'emotion_Happy':"H",
                        'emotion_Neutral':"N",
                        'emotion_Sad':"SA",
                        'emotion_Surprise':"SU"}

def send_request(ne,ns,em):
    data["new_emotion"]=ne
    data["new_sentence"]=ns
    data["emotion"]=emotion_dict_interface[em]
    resp=requests.put(url+'update_input', json=data, headers=headers)
    print("sent")

    

if __name__ == "__main__":
    t=0
    while t<100:
       t+=1
       
    send_request("True","True",'emotion_Disgust')


"""
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

data={
    "emotion":"",
    "new_sentence":"False",
    "new_emotion":"False"
}
new_sentence_input="False"
new_emotion_input="False"
emotion_input=""

emotion_dict_interface={'emotion_Angry':"A", 
                        'emotion_Disgust':"D",
                        'emotion_Fear':"F", 
                        'emotion_Happy':"H",
                        'emotion_Neutral':"N",
                        'emotion_Sad':"SA",
                        'emotion_Surprise':"SU"}

@app.route ('/update_input', methods = ['PUT'] )  
def update_input():
        global new_sentence_input, emotion_input, new_emotion_input
        updated_data = request.get_json()
        data.update(updated_data)
        new_sentence_input=data["new_sentence"]
        new_emotion_input=data["new_emotion"]
        emotion_input=emotion_dict_interface[data["emotion"]]
        print("updated input",data)
        return jsonify(data)

@app.route ('/get_input', methods = ['PUT'] )  
def get_input():
        global new_sentence_input, emotion_input, new_emotion_input
        updated_data = request.get_json()
        data.update(updated_data)
        data["new_sentence"]=new_sentence_input
        data["new_emotion"]=new_emotion_input
        data["emotion"]=emotion_input
        print("get input",data)
        return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5020, debug=True)


