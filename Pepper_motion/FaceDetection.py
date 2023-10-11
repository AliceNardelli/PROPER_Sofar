import random
import socket, select
from time import gmtime, strftime
from random import randint
import cv2
import subprocess
import cvlib as cv
import os


threshold=0

 

def PeopleDetection():
    image1 = cv2.imread("/home/alice/images/imag0.png")
    
    #crop possibile
    faces1, confidences1 = cv.detect_face(image1,0.18,enable_gpu=True)
    #print(confidences1)
    counter=len(confidences1)
    # loop through detected faces
    for face,conf in zip(faces1,confidences1):

        (startX,startY) = face[0],face[1]
        (endX,endY) = face[2],face[3]
        #print(endY-startY)
        if (endY-startY)>threshold:
           cv2.rectangle(image1, (startX,startY), (endX,endY), (0,255,0), 2)
        else:
            counter-=1

    # save output


    cv2.imwrite("/home/alice/test.png", image1)
    cv2.imshow("peopleperc",image1)
    cv2.waitKey(5000)
    

    if counter>2:
        counter=2
    return counter

if __name__ == '__main__':

                detected_people=PeopleDetection()

                print(detected_people)
                