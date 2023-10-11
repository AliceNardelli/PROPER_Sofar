# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import qi
import os
import sys
import argparse
import time
import requests
url='http://127.0.0.1:5010/'
headers= {'Content-Type':'application/json'}

data={
      "body":"",
      "state":""
}



def touch_detected(value): #esempio di callback
        global touched
        touched=True
        data["body"]=value[0][0]
        data["state"]=value[0][1]
        resp=requests.put(url+'tactile_interface', json=data, headers=headers)
        

if __name__ == '__main__':
    global touched
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.182",
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

    tts2=session.service("ALMemory")
    touched=False
    touch = tts2.subscriber("TouchChanged") #questo permette la callback
    connection = touch.signal.connect(touch_detected) #segnale della sottoscrizione
    while True:
            time.sleep(1)
            if touched:
                touched =False

    
            
         
 