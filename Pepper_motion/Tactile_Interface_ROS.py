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
tt=False
app = Flask(__name__)

data={
    "image":"",
}


@app.route ('/tactile_interface', methods = ['PUT'] )   
def face_detector():
    global pub_touch,tt
    updated_data = request.get_json()
    data.update(updated_data)
    if data["state"]==True:
        print("Touched")
        tt=True
    else:
        tt=False
    while tt==True:
        pub_touch.publish("True")
    data["image"]="ok"
    return jsonify(data)


if __name__ == "__main__":
    global pub_touch
    rospy.init_node('tactile_interface')
    pub_touch = rospy.Publisher('/touch', String, queue_size=10)
    app.run(host='0.0.0.0', port=5010, debug=True)
   