from flask import Flask, request, jsonify
app = Flask(__name__)


data={
    "x":0,
}


class Move:
    def __init__(self):
        print("Class move")

    def motion(self):
        print("I am navigating")



@app.route ('/navigation_server', methods = ['PUT'] )   
def move():
    global m
    updated_data = request.get_json()
    data.update(updated_data)
    m.motion()
    return jsonify(data)

if __name__ == '__main__':
    global m
    m=Move()
    app.run(host='0.0.0.0', port=5008, debug=True)
    
