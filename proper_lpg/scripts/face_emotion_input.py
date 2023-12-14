#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from flask import Flask, request, jsonify
from proper_lpg.msg import Emotions
import rospy
import threading
size_window=10

app = Flask(__name__)

data={
        "emotion":"",
        "new_emotion":"False",
}

window_emotion=[]

emotion_dict_interface={'Angry':"A", 
                        'Disgust':"D",
                        'Fear':"F", 
                        'Happy':"H",
                        'Neutral':"N",
                        'Sad':"SA",
                        'Surprise':"SU"}



@app.route ('/update_input', methods = ['PUT'] )  
def update_input():
        updated_data = request.get_json()
        data.update(updated_data)
        
        if data["new_emotion"]=="True": 
            window_emotion.append(emotion_dict_interface[data["emotion"]])
            if len(window_emotion)>size_window:
               last=window_emotion.pop(0)
            e=max(set(window_emotion), key=window_emotion.count)
            em_msg=Emotions()
            em_msg.emotion=e
            em_msg.w_emotions=window_emotion
            pub.publish(em_msg)
        
        print("updated input",data)
        return jsonify(data)




if __name__ == "__main__":
    threading.Thread(target=lambda: rospy.init_node('test_node', disable_signals=True)).start()
    pub = rospy.Publisher('/face_emotion', Emotions, queue_size=10)
    app.run(host='0.0.0.0', port=5024, debug=True)
   
    


