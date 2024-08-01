#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from flask import Flask, request, jsonify

app = Flask(__name__)

data={ 
    "restart":"False"
}

restart="False"


@app.route ('/set_restart', methods = ['PUT'] )  
def set_restart():
        global restart, data
        updated_data = request.get_json()
        data.update(updated_data) 
        restart="True"     
        return jsonify(data)


@app.route ('/get_restart', methods = ['PUT'] )  
def get_restart():
        global restart, data
        if restart=="True":
               data["restart"]="True"
               restart="False"
        else:
               data["restart"]="False"
        return jsonify(data)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5018, debug=True)


