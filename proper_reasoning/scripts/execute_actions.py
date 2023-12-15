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
        "new_action":"",
        "executed":"",
        "result":"",
        "finished":""

}

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
        else:
            data["new_action"]="False" 
        print(data)
        return jsonify(data)


@app.route ('/set_exec', methods = ['PUT'] )  
def set_exec():
        global executed, new_action
        updated_data = request.get_json()
        data["result"]=updated_data["result"]
        executed="True"
        data["new_action"]="False"
        new_action="False" 
        return jsonify(data)



@app.route ('/get_exec', methods = ['PUT'] )  
def get_exec():
        global executed
        if executed=="True":
            data["executed"]="True"  
            executed="False" 
        else:
            data["executed"]="False" 
        data["new_action"]="False"
        return jsonify(data)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5021, debug=False)