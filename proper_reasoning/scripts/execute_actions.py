#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from flask import Flask, request, jsonify




app = Flask(__name__)

data={
        "action":"",
        "language":"",
        "personality":"",
        "pitch":"",
        "volume":"",
        "velocity":"",
        "head":"",
        "gaze":"",
        "new_action":"",
        "executed":"",
        "result":"",
        "finished":"",
        "timestamp":str(-1)
}
prev_timestamp=str(-1)
new_action="False"
executed="False"

@app.route ('/set_action', methods = ['PUT'] )  
def set_action():
        global new_action
        updated_data = request.get_json()
        data.update(updated_data)
        if data["new_action"]=="True":
            new_action="True"
        return jsonify(data)



@app.route ('/get_action', methods = ['PUT'] )  
def get_action():
        global new_action
        print(data)
        if new_action=="True":
            data["new_action"]="True" 
            new_action="False"  
        else:
            data["new_action"]="False" 
        
        return jsonify(data)


@app.route ('/set_exec', methods = ['PUT'] )  
def set_exec():
        global executed, new_action, prev_timestamp
        updated_data = request.get_json()
        data["result"]=updated_data["result"]
        executed="True"
        data["new_action"]="False"
        #new_action="False" 
        prev_timestamp=data["timestamp"]
        
        return jsonify(data)



@app.route ('/set_exec_new', methods = ['PUT'] )  
def set_exec_new():
        global executed, new_action, prev_timestamp
        if new_action=="True":
              data["result"]="True"
              executed="True"
              data["new_action"]="False"
              new_action="False"
              data["timestamp"]=prev_timestamp
        return jsonify(data)



@app.route ('/get_exec', methods = ['PUT'] )  
def get_exec():
        global executed, prev_timestamp
        if executed=="True":
            data["executed"]="True"  
            executed="False" 
            
        else:
            data["executed"]="False" 
        data["new_action"]="False"
        return jsonify(data)


@app.route ('/reset_timestamp', methods = ['PUT'] )  
def time_reset():
        data["timestamp"]=str(-1)
        print(data)
        return jsonify(data)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5021, debug=False)