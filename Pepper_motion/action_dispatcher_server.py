from flask import Flask, request, jsonify
from class_navigation import *
from class_gesture import *
app = Flask(__name__)


data={
    "action":"",
}

@app.route ('/navigation_server', methods = ['PUT'] )   
def mm():
    global m
    updated_data = request.get_json()
    data.update(updated_data)
    m.move(data["action"],data["params"])
    return jsonify(data)

@app.route ('/gesture_server', methods = ['PUT'] )   
def gg():
    global g
    updated_data = request.get_json()
    data.update(updated_data)
    g.gesture(data["action"],data["params"])
    return jsonify(data)

if __name__ == '__main__':
    global m
    m=Move()
    g=Gesture()
    app.run(host='0.0.0.0', port=5008, debug=True)
    
