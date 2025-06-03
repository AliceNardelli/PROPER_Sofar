from flask import Flask, request, jsonify, abort
from flask_cors import CORS # Import the CORS extension
from client_proper import *
from problem_param import *
import requests
import numpy as np

app = Flask(__name__)
CORS(app)

client_proper=ClientProper()

new_perception = False
user_emotion = ""
user_sentence = ""
user_episodes = ""
#distance, gaze??

traits=["Extrovert","Introvert","Conscientious","Distracted","Agreeable","Disagreeable"]
weights = [0,0,0,0,0,0]
comfortability = 5
emotion_mask={
    "A":[4,2,3,1,5,5],
    "H":[4,2,1,1,5,5],
    "S":[2,2,1,1,5,2],
    "C":[4,4,1,1,5,5],
    "N":[4,4,1,1,4,4],
}


@app.route('/api/post_personality', methods=['POST'])
def received_agent_personality():
    if not request.json:
        abort(400)
    global traits, weights
    frame_payload = request.json
    if frame_payload["personality"]!="":
        i = 0
        for p in frame_payload["personality"]:
            if p in traits[i]:
                weights[i] +=1
            i +=1
    return ''


@app.route('/api/get_em_description', methods=['GET'])
def get_em():
    em_description="" #INSERT MEM DESCRIPTION
    payload = {
        "em_descrption":em_description
    }
    return jsonify(payload)


@app.route('/api/post_perception', methods=['POST'])
def received_user_perception():
    if not request.json:
        abort(400)
    global new_perception, user_emotion, user_sentence, user_episodes

    frame_payload = request.json
    
    if frame_payload["user"]!="":
        new_perception=True
        user_emotion=frame_payload["emotion"]
        user_sentence =frame_payload["sentence"]
        user_episodes =frame_payload["episodes"]
        proper_llm(new_perception, user_emotion, user_sentence, user_episodes)
    return ''
    

def proper_llm(new_perception, user_emotion, user_sentence, user_episodes):
    global comfortability, emotion_weights
    actions = []
    if new_perception:
        new_perception=False
        #PROSPECTION
        #actions = propection()
        #comfortability = X

    while actions!=[] and new_perception==False:
        action = actions.pop(0)
        #PESONALITY GENERATOR
        #EMOTION
        mask_weights=emotion_mask[map_emotion_AV_axis[user_emotion]]
        emotion_weights=np.multiply(mask_weights, weights)
        
        sum_em_weights=0
        for ew in emotion_weights:
            sum_em_weights+=ew

        
        ind=0
        for ew in emotion_weights:
            emotion_weights[ind]=ew/sum_em_weights
            ind+=1

        
        personality_emotions=np.random.choice(traits,p=emotion_weights)

        agent_emotion= ""
        language_style =""
        gaze_behavior = ""
        client_proper.post_action(action, agent_emotion, language_style, gaze_behavior)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2013)