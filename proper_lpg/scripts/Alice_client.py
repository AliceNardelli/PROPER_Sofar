#!/usr/bin/env python3 -tt
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET
import requests
import argparse
import socket
import os
import re
import zlib
import sys
import json
import xml
import rospy
from std_msgs.msg import String
from proper_lpg.msg import Emotions
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
from flask import Flask, request, jsonify


tokenizer = AutoTokenizer.from_pretrained('MilaNLProc/feel-it-italian-emotion')
model = AutoModelForSequenceClassification.from_pretrained('MilaNLProc/feel-it-italian-emotion')

emotion_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Location of the server
cineca = "131.175.205.146"
local = "127.0.0.1"
#local="130.251.13.101"
server_ip = cineca
audio_recorder_ip = local
registration_ip = local
port = "5000"
BASE = "http://" + cineca + ":" + port + "/CAIR_hub"
min_registered_users_number = 1
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try to connect to the socket that listens to the user speech
try:
    client_socket.settimeout(10)
    print("Attempting to connect to the socket...")
    client_socket.connect((audio_recorder_ip, 9090))
    client_socket.settimeout(30)
    #client_socket.setblocking(0)   
except ConnectionError:
    print("Check socket connection with audio_recorder.py")
    sys.exit(1)


activated=True


sentence =""

data = {
    "activated": "p",
    "response": "s",
}


app = Flask(__name__)

@app.route ('/listener', methods = ['PUT'] )
def listener():
    updated_data = request.get_json()
    data.update(updated_data)
    if data["activated"]=="True":
        res=get_sentence()
        data["response"]=res
        return jsonify(data)

     


def get_sentence():
    global speech_pub
    client_socket.send("Hello".encode('utf-8'))
    print("hello there")
    try:
            xml_string = client_socket.recv(1024).decode('utf-8')
            if xml_string == "":
                print("Socket error")
                sys.exit(1)

            # Do not proceed until the xml string is complete and all tags are closed
            proceed = False
            while not proceed:
                try:
                    tree=ET.ElementTree(ET.fromstring(xml_string))
                    sentence = str(tree.findall('profile_id')[0].text)
                    proceed = True
                except UnicodeEncodeError:
                    sentence=xml_string.split(">")[2].replace("<speaking_time","")
                    proceed = True
                except xml.etree.ElementTree.ParseError:
                    # If the xml is not complete, read again from the socket
                    print("The XML is not complete.")
                    xml_string = xml_string + client_socket.recv(1024).decode('utf-8')
            input_sentence=str(sentence.encode("utf-8"))
            print(input_sentence)
            out=emotion_analysis(input_sentence,top_k=9)
            we=[]
            pp=[]
            for o in out:
                we.append(o["label"]) 
                pp.append(o["score"])
            em_msg=Emotions()
            em_msg.w_emotions=we
            em_msg.probs=pp
            speech_pub.publish(em_msg)
            return input_sentence

    except socket.timeout:
            print("timeout")

            

if __name__ == '__main__':
    global speech_pub
    # Define the program description
    text = 'This is the client for CAIR.'
    speech_pub = rospy.Publisher('/speech_emotion', Emotions, queue_size=10)
    # Initiate the parser with a description
    parser = argparse.ArgumentParser(description=text)
    # Add long and short argument
    parser.add_argument("--language", "-l", help="set the language of the client to it or en")
    # Read arguments from the command line
    args = parser.parse_args()
    if not args.language:
        print("No language provided. The default English language will be used.")
        language = "en"
    else:
        language = args.language
        print("The language has been set to", language)
   
    rospy.init_node('sentence_emotion_detection')
    app.run(host='0.0.0.0', port=5011, debug=True)
