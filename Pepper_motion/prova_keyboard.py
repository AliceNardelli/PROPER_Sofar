
import os

# Set cache directories for XDG and Hugging Face Hub
os.environ['XDG_CACHE_HOME'] = '/home/alice/.cache'
os.environ['HUGGINGFACE_HUB_CACHE'] = '/home/alice/.cache'

import torch

# Set device to GPU if available, otherwise use CPU
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
from tqdm.notebook import tqdm
import torch

from transformers import (AutoFeatureExtractor,
                          AutoModelForImageClassification,
                          AutoConfig)

from PIL import Image, ImageDraw
import random
import socket, select
from time import gmtime, strftime
from random import randint
import cv2
import subprocess
import cvlib as cv
import os
import rospy
import time
from std_msgs.msg import String

folder="/home/alice/images/"
focal_length = 1584  # Set the focal length based on your camera specifications
avg_face_width = 14  # Set the average width of a face in centimeters

# Load the pre-trained model and feature extractor
extractor = AutoFeatureExtractor.from_pretrained(
    "trpakov/vit-face-expression"
    #"RickyIG/emotion_face_image_classification"
)
model = AutoModelForImageClassification.from_pretrained(
    "trpakov/vit-face-expression"
    #"RickyIG/emotion_face_image_classification"
)


def measure_distance(face_width_pixels):
    return (avg_face_width * focal_length) / face_width_pixels


def detect_emotions(image):
    # apply face detection
    try:
        faces, confidences = cv.detect_face(image)
        # loop through detected faces
        for face, conf in zip(faces,[confidences[0]]):
            (startX,startY) = face[0],face[1]
            (endX,endY) = face[2],face[3]
            # draw rectangle over face
            cv2.rectangle(image, (startX,startY), (endX,endY), (0,255,0), 2)

            # Calculate the width of the detected face in pixels
            face_width_pixels = endX-startX

            # Measure the distance to the detected face
            distance = measure_distance(face_width_pixels)

            # Display the distance above the face rectangle
            #cv2.putText(image, f"{distance:.2f} cm", (startX+5, startY ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            #image = cv2.putText(image,"Distance: "+str(distance), (startX+5, startY ), cv2.FONT_HERSHEY_SIMPLEX , 1,  (0, 255, 0), 2, cv2.LINE_AA)
            
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            inputs = extractor(images=image, return_tensors="pt")

            # Pass the pre-processed face through the model to
            # get emotion predictions
            outputs = model(**inputs)

            # Apply softmax to the logits to get probabilities
            probabilities = torch.nn.functional.softmax(outputs.logits,
                                                        dim=-1)

            # Retrieve the id2label attribute from the configuration
            id2label = AutoConfig.from_pretrained(
                "trpakov/vit-face-expression"
                #"RickyIG/emotion_face_image_classification"
            ).id2label

            #print(id2label)
            # Convert probabilities tensor to a Python list
            probabilities = probabilities.detach().numpy().tolist()[0]
            max_em=max(probabilities)
            ind=probabilities.index(max_em)
            em=id2label[ind]
            print("Emotion: "+str(em))
            return image, em, distance

    except:
        return "", "", 0


if __name__ == "__main__":
    rospy.init_node('webcam_emotion_detection')
    pub = rospy.Publisher('/emotion', String, queue_size=10)
    #video = cv2.VideoCapture(0) #webcam
    video = cv2.VideoCapture(2) #external webcam
    time.sleep(2.0)
    window_emotion=[] 
    size_window=5

    while not rospy.is_shutdown():
        ret, frame = video.read()
        
        if ret is False:
            break


        h, w, _ = frame.shape

        width=1000
        height = int(width*(h/w))
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)
        
        image, em, distance=detect_emotions(frame)
        if image!="":
            # text 
            text = "Emotion: "+ em + " Distance: "+ str(distance)
            
            # font 
            font = cv2.FONT_HERSHEY_SIMPLEX 
            
            # org 
            org = (00, 185) 
            
            # fontScale 
            fontScale = 1
            
            # Red color in BGR 
            color = (0, 0, 255) 
            
            # Line thickness of 2 px 
            thickness = 2
            
            # Using cv2.putText() method 
            image = cv2.putText(image, text, org, font, fontScale,  color, thickness, cv2.LINE_AA, False) 
            cv2.imshow("Image", image)
            window_emotion.append(em)
            if len(window_emotion)>size_window:
               last=window_emotion.pop(0)
            e=max(set(window_emotion), key=window_emotion.count)
            print(window_emotion,e)
            pub.publish(e)
        else:
            cv2.imshow("Image", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break


    cv2.destroyAllWindows()
    video.release()