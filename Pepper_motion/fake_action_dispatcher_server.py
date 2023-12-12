# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

app = Flask(__name__)

data={
    "action":"",
}

@app.route ('/navigation_server', methods = ['PUT'] )   
def mm():
    updated_data = request.get_json()
    data.update(updated_data)
    print(data)
    return jsonify(data)

@app.route ('/gesture_server', methods = ['PUT'] )   
def gg():
    updated_data = request.get_json()
    data.update(updated_data)
    print(data)
    return jsonify(data)

@app.route ('/speak_server', methods = ['PUT'] )   
def ss():
    updated_data = request.get_json()
    data.update(updated_data)
    print(data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)