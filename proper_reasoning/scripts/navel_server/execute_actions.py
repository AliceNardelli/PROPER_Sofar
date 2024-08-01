#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from flask import Flask, request, jsonify

app = Flask(__name__)

data_action={
        "robot_emotion":"",
        "sentence":"",
        "volume":"",
        "gaze":"",
        "tone":"",
        "gesture_amplitude":"",
        "head":""
         
}


@app.route ('/exec_action', methods = ['PUT'] )  
def set_exec():
        global executed, new_action, prev_timestamp
        updated_data = request.get_json()
        print(updated_data)
        return jsonify(updated_data)







if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5019, debug=False)