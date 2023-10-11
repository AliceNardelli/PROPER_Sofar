import os
import numpy as np
import subprocess
import os
import rospy
from flask import Flask, request, jsonify

app = Flask(__name__)

data={
    "image":"",
}


@app.route ('/tactile_interface', methods = ['PUT'] )   
def face_detector():
    updated_data = request.get_json()
    data.update(updated_data)
    print(data)
    data["image"]="ok"
    return jsonify(data)




if __name__ == "__main__":
    #rospy.init_node('face_detector')
    #s = rospy.Service('action_dispatcher_srv', ExecAction, dispatch_action)
    print("Ready to add two ints.")
    #rospy.spin()
    app.run(host='0.0.0.0', port=5010, debug=True)