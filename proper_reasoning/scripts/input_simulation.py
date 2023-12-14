#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from flask import Flask, request, jsonify

app = Flask(__name__)

data={
        "emotion":"N",
        "new_sentence":"False",
        "new_emotion":"False",
        "new_attention":"False",
        "attention":"",
        "update":"False",
}

window=[]
window_size=10
new_sentence_input="False"
new_emotion_input="False"
new_attention_input="False"
emotion_input=""
attention_input=""
emotion_dict_interface={'Angry':"A", 
                        'Disgust':"D",
                        'Fear':"F", 
                        'Happy':"H",
                        'Neutral':"N",
                        'Sad':"SA",
                        'Surprise':"SU"}



@app.route ('/update_input', methods = ['PUT'] )  
def update_input():
        global new_sentence_input, emotion_input, new_emotion_input, new_attention_input, attention_input
        updated_data = request.get_json()
        data.update(updated_data)
        if data["new_sentence"]=="False":  
                if new_sentence_input!="True":
                       new_sentence_input=data["new_sentence"]
        else:
            new_sentence_input=data["new_sentence"]
        if data["new_emotion"]=="False":
                if (new_emotion_input!="True"):
                       new_emotion_input=data["new_emotion"]
                       emotion_input=emotion_dict_interface[data["emotion"]]
             
        else:
               new_emotion_input=data["new_emotion"]
               emotion_input=emotion_dict_interface[data["emotion"]]
               
        if data["new_attention"]=="False":  
                if new_attention_input!="True":
                       new_attention_input=data["new_attention"]
                       attention_input=data["attention"]
        else:
                       new_attention_input=data["new_attention"]
                       attention_input=data["attention"]
        
        """
        print("new emotion", new_emotion_input)
        print("emotion", emotion_input)
        print("new attention", new_attention_input)
        print("attention", attention_input)
        print("new sentence", new_sentence_input)
        """
        return jsonify(data)



@app.route ('/get_input', methods = ['PUT'] )  
def get_input():
        global new_sentence_input, emotion_input, new_emotion_input, new_attention_input, attention_input
        updated_data = request.get_json()
        data.update(updated_data)
        d=data["update"]
        data["new_sentence"]=new_sentence_input
        data["new_emotion"]=new_emotion_input
        data["emotion"]=emotion_input
        data["new_attention"]=new_attention_input
        data["attention"]=attention_input
        print("get input",data)
        if d=="True":
                new_sentence_input="False"
                new_emotion_input="False"
                new_attention_input="False"
        return jsonify(data)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5020, debug=True)
   
    


