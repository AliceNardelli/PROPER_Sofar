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
from flask import Flask, request, jsonify

app = Flask(__name__)

data={
    "image":"",
}
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

@app.route ('/face_detector', methods = ['PUT'] )   
def face_detector():
    updated_data = request.get_json()
    data.update(updated_data)
    image=cv2.imread(folder+data["image"])
    detect_emotions(image)
    data["image"]="ok"
    return jsonify(data)

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
            print("Distance: "+str(distance))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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

            print(id2label)
            # Convert probabilities tensor to a Python list
            probabilities = probabilities.detach().numpy().tolist()[0]

            # Map class labels to their probabilities
            class_probabilities = {id2label[i]: prob for i,
                                prob in enumerate(probabilities)}

            # Define colors for each emotion
            colors = {
                "angry": "red",
                #"anger": "red",
                #"contempt":"red",
                "disgust": "green",
                "fear": "gray",
                "happy": "yellow",
                "neutral": "purple",
                "sad": "blue",
                "surprise": "orange"
            }
            palette = [colors[label] for label in class_probabilities.keys()]

            # Prepare a figure with 2 subplots: one for the face image,
            # one for the bar plot
            fig, axs = plt.subplots(1, 2, figsize=(15, 6))

            # Display the cropped face in the left subplot
            axs[0].imshow(np.array(image))
            axs[0].axis('off')

            # Create a horizontal bar plot of the emotion probabilities in
            # the right subplot
            sns.barplot(ax=axs[1],
                        y=list(class_probabilities.keys()),
                        x=[prob * 100 for prob in class_probabilities.values()],
                        palette=palette,
                        orient='h')
            axs[1].set_xlabel('Probability (%)')
            axs[1].set_title('Emotion Probabilities')
            axs[1].set_xlim([0, 100])  # Set x-axis limits to show percentages
            # Show the plot
            plt.show()
    except:
        print("face not detecteds")


if __name__ == "__main__":
    #rospy.init_node('face_detector')
    #s = rospy.Service('action_dispatcher_srv', ExecAction, dispatch_action)
    print("Ready to add two ints.")
    #rospy.spin()
    app.run(host='0.0.0.0', port=5009, debug=True)