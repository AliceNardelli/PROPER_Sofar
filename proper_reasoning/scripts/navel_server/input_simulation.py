#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from flask import Flask, request, jsonify
import random
import numpy as np
app = Flask(__name__)

data={
        "emotion":"N",
        "new_sentence":"False",
        "new_emotion":"False",
        "new_attention":"False",
        "attention":"",
        "update":"False",
}


emotions=["A","D","F","H","N","SA","SU","","","",""]
Attention=["positive","negative","","","",""]
Sentence=["Hi",""]

@app.route ('/get_input', methods = ['PUT'] )  
def get_input():
        updated_data = request.get_json()
        data.update(updated_data)
        em=np.random.choice(emotions)
        if em != "":
              data["new_emotion"]="True"
              data["emotion"]=em
        else:
              data["new_emotion"]="False"
              data["emotion"]=em

        attention=np.random.choice(Attention)
        if attention != "":
              data["new_attention"]="True"
              data["attention"]=attention
        else:
              data["new_attention"]="False"
              data["attention"]=attention

        sentence=np.random.choice(Sentence)
        if sentence != "":
              data["new_sentence"]="True"
              data["sentence"]=sentence
        else:
              data["new_sentence"]="False"
              data["sentence"]=sentence
              
        return jsonify(data)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5020, debug=True)
   
    


