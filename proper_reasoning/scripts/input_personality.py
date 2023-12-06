#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from flask import Flask, request, jsonify

app = Flask(__name__)

data={       
        "new_personality":"False",
        "Extrovert":0,
        "Introvert":0,
        "Agreeable":0,
        "Disagreeable":0,
        "Conscientious":0,
        "Unscrupolous":0,
}

new_personality="False"




@app.route ('/set_personality', methods = ['PUT'] )  
def set_personality():
        global data, new_personality
        updated_personality = request.get_json()
        data.update(updated_personality) 
        print("SET_NEW_PERSONALITY")
        print(data)
        new_personality="True"     
        return jsonify(data)


@app.route ('/get_personality', methods = ['PUT'] )  
def get_personality():
        global data, new_personality
        if new_personality=="True":
               data["new_personality"]="True"
               new_personality="False"
               print("GET_NEW_PERSONALITY")
               print(data)
        else:
               data["new_personality"]="False"
        
        return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5019, debug=True)


