from flask import Flask, request, jsonify
from class_navigation import *
from class_gesture import *
from class_speak import *
import qi
app = Flask(__name__)

data={
    "action":"",
}

@app.route ('/navigation_server', methods = ['PUT'] )   
def mm():
    global m
    updated_data = request.get_json()
    data.update(updated_data)
    #m.move(data["action"],data["params"])
    return jsonify(data)

@app.route ('/gesture_server', methods = ['PUT'] )   
def gg():
    global g
    updated_data = request.get_json()
    data.update(updated_data)
    g.gesture(data["action"],data["params"])
    return jsonify(data)

@app.route ('/speak_server', methods = ['PUT'] )   
def ss():
    global s
    updated_data = request.get_json()
    data.update(updated_data)
    s.speak(data["action"],data["personality"],data["params"])
    return jsonify(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.140",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))        
        #app = qi.Application(["TabletModule", "--qi-url=" + "tcp://" + args.ip + ":" + str(args.port)])
        #app.start()
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    m=Move(session)
    g=Gesture(session)
    s=Speak(session)
    app.run(host='0.0.0.0', port=5008, debug=True)
    
