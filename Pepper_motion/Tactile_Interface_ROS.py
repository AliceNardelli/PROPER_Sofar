import os
import numpy as np
import subprocess
import os
import rospy
from flask import Flask, request, jsonify
from std_msgs.msg import String
from multiprocessing import Process
import time
server=None

app = Flask(__name__)

data={
    "image":"",
}


@app.route ('/tactile_interface', methods = ['PUT'] )   
def face_detector():
    global pub
    updated_data = request.get_json()
    data.update(updated_data)
    if data["state"]==True:
        print("Touched")
        pub.publish("True")
    data["image"]="ok"
    return jsonify(data)


if __name__ == "__main__":
    global pub
    rospy.init_node('tactile_interface')
    pub = rospy.Publisher('/touch', String, queue_size=10)
    app.run(host='0.0.0.0', port=5010, debug=True)
   