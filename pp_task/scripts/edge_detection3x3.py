import numpy as np
import cv2 
import signal 
import sys
from pynput import keyboard
import rospy
from pp_task.msg import Board

rectangles={
    "area1":{"x":0,"y":0,"w":0,"h":0,"name":""},
    "area2":{"x":0,"y":0,"w":0,"h":0,"name":""},
    "area3":{"x":0,"y":0,"w":0,"h":0,"name":""},
    "area4":{"x":0,"y":0,"w":0,"h":0,"name":""},
    "area5":{"x":0,"y":0,"w":0,"h":0,"name":""},
    "area6":{"x":0,"y":0,"w":0,"h":0,"name":""},
    "area7":{"x":0,"y":0,"w":0,"h":0,"name":""},
    "area8":{"x":0,"y":0,"w":0,"h":0,"name":""},
    "area9":{"x":0,"y":0,"w":0,"h":0,"name":""},
}
areas=["area1","area2","area3","area4","area5","area6","area7","area8","area9"]
init=True
def define_contours(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    blurred = cv2.GaussianBlur(src=gray, ksize=(3, 5), sigmaX=0.5)
    edged = cv2.Canny(blurred, 30, 200)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print("Number of Contours found = " + str(len(contours)))
    i=0
    #cv2.drawContours(image, contours, -1, (0, 255, 0), 3) 
    for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 800):
                x, y, w, h = cv2.boundingRect(contour)
                image = cv2.rectangle(image, (x, y),  (x + w, y + h), (255, 0, 0), 8)
                try:
                    image = cv2.putText(image, areas[i], (x,y),  cv2.FONT_HERSHEY_SIMPLEX,  1, (255, 0, 0) , 2, cv2.LINE_AA)
                    rectangles[areas[i]]["x"]=x
                    rectangles[areas[i]]["y"]=y
                    rectangles[areas[i]]["w"]=w
                    rectangles[areas[i]]["h"]=h
                    i+=1
                except:
                    print("more than needd are found")

                
    return image

    
def green_detection(imageFrame):
    # Convert the imageFrame in  
    # BGR(RGB color space) to  
    # HSV(hue-saturation-value) 
    # color space 
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

    # Set range for green color and  
    # define mask 
    green_lower = np.array([25, 52, 72], np.uint8) 
    green_upper = np.array([102, 255, 255], np.uint8) 
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 
  
  
    # Morphological Transform, Dilation 
    # for each color and bitwise_and operator 
    # between imageFrame and mask determines 
    # to detect only that particular color 
    kernel = np.ones((5, 5), "uint8") 
      

    # For green color 
    green_mask = cv2.dilate(green_mask, kernel) 
    res_green = cv2.bitwise_and(imageFrame, imageFrame, 
                                mask = green_mask) 
           
  
    # Creating contour to track green color 
    contours, hierarchy = cv2.findContours(green_mask, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE) 
      

    return contours           
    #return imageFrame

def red_detection(imageFrame):
    # Convert the imageFrame in  
    # BGR(RGB color space) to  
    # HSV(hue-saturation-value) 
    # color space 
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

    # Set range for green color and  
    # define mask 
    green_lower = np.array([120, 75, 100], np.uint8) #[136, 87, 111]
    green_upper = np.array([180, 255, 255], np.uint8) 
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 
  
  
    # Morphological Transform, Dilation 
    # for each color and bitwise_and operator 
    # between imageFrame and mask determines 
    # to detect only that particular color 
    kernel = np.ones((5, 5), "uint8") 
      

    # For green color 
    green_mask = cv2.dilate(green_mask, kernel) 
    res_green = cv2.bitwise_and(imageFrame, imageFrame, 
                                mask = green_mask) 
           
  
    # Creating contour to track green color 
    contours, hierarchy = cv2.findContours(green_mask, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE) 
      

    return contours           
    #return imageFrame

def blue_detection(imageFrame):
    # Convert the imageFrame in  
    # BGR(RGB color space) to  
    # HSV(hue-saturation-value) 
    # color space 
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

    # Set range for green color and  
    # define mask 
    green_lower = np.array([100,150,0], np.uint8) 
    green_upper = np.array([140, 255, 255], np.uint8) 
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 
  
  
    # Morphological Transform, Dilation 
    # for each color and bitwise_and operator 
    # between imageFrame and mask determines 
    # to detect only that particular color 
    kernel = np.ones((5, 5), "uint8") 
      

    # For green color 
    green_mask = cv2.dilate(green_mask, kernel) 
    res_green = cv2.bitwise_and(imageFrame, imageFrame, 
                                mask = green_mask) 
           
  
    # Creating contour to track green color 
    contours, hierarchy = cv2.findContours(green_mask, 
                                           cv2.RETR_TREE, 
                                           cv2.CHAIN_APPROX_SIMPLE) 
      

    return contours           
    #return imageFrame




def key_press(key):
    global init
    print(f'Pressed {key}')
    init=False

    
def main(): 
    rospy.init_node("board_state_publisher")
    board_pub = rospy.Publisher('/board_state', Board, queue_size=10)
    # Open the default webcam  
    cap = cv2.VideoCapture()
    cap.open("/dev/video2")
    listener = keyboard.Listener(on_press=key_press)
    listener.start()
    #detecting area while a keyboard is inserted
    while init: 
        # Read a frame from the webcam 
        ret, frame = cap.read() 
        if not ret: 
            print('Image not captured') 
            break
        bd = define_contours(frame)
        cv2.imshow("Edges", bd) 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        # Perform Canny edge detection on the frame
    #ordering areas
    x_values=[]
    reverse_dict_x={}
    reverse_dict_y={}
    y_values=[]
    for x in rectangles.keys():
        x_values.append(int(rectangles[x]["x"]))
        reverse_dict_x[int(rectangles[x]["x"])]=x
        y_values.append(int(rectangles[x]["y"]))
        reverse_dict_y[int(rectangles[x]["y"])]=x
    x_values.sort()  
    y_values.sort()
    #column1
    xxx=[x_values[0],x_values[1],x_values[2]]
    ar=[reverse_dict_x[xxx[0]],reverse_dict_x[xxx[1]],reverse_dict_x[xxx[2]]]
    yyy=[rectangles[ar[0]]["y"],rectangles[ar[1]]["y"],rectangles[ar[2]]["y"]]
    index=[0,1,2]
    index_min=yyy.index(min(yyy))
    rectangles[ar[index_min]]["name"]="A1"
    index.remove(index_min)
    index_max=yyy.index(max(yyy))
    rectangles[ar[index_max]]["name"]="A7"
    index.remove(index_max)
    rectangles[ar[index[0]]]["name"]="A4"
    print(rectangles)
    #column2
    xxx=[x_values[3],x_values[4],x_values[5]]
    ar=[reverse_dict_x[xxx[0]],reverse_dict_x[xxx[1]],reverse_dict_x[xxx[2]]]
    yyy=[rectangles[ar[0]]["y"],rectangles[ar[1]]["y"],rectangles[ar[2]]["y"]]
    index=[0,1,2]
    index_min=yyy.index(min(yyy))
    rectangles[ar[index_min]]["name"]="A2"
    index.remove(index_min)
    index_max=yyy.index(max(yyy))
    rectangles[ar[index_max]]["name"]="A8"
    index.remove(index_max)
    rectangles[ar[index[0]]]["name"]="A5"
    print(rectangles)
    #column3
    xxx=[x_values[6],x_values[7],x_values[8]]
    ar=[reverse_dict_x[xxx[0]],reverse_dict_x[xxx[1]],reverse_dict_x[xxx[2]]]
    yyy=[rectangles[ar[0]]["y"],rectangles[ar[1]]["y"],rectangles[ar[2]]["y"]]
    index=[0,1,2]
    index_min=yyy.index(min(yyy))
    rectangles[ar[index_min]]["name"]="A3"
    index.remove(index_min)
    index_max=yyy.index(max(yyy))
    rectangles[ar[index_max]]["name"]="A9"
    index.remove(index_max)
    rectangles[ar[index[0]]]["name"]="A6"
    print(rectangles)
   
    

    while True:
         ret, frame = cap.read() 
         for x in rectangles.keys():
            
            ss=(int(rectangles[x]["x"]),int(rectangles[x]["y"]))
            se=(int(rectangles[x]["x"])+int(rectangles[x]["w"]), int(rectangles[x]["y"])+int(rectangles[x]["h"]))
            frame = cv2.rectangle(frame, ss,  se, (0, 255, 0), 8)
            frame = cv2.putText(frame, str(rectangles[x]["name"]), (int(rectangles[x]["x"]),int(rectangles[x]["y"])),  cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 255, 0) , 2, cv2.LINE_AA)
         
         board_msg=Board()
         board_msg.area1=""
         board_msg.area2=""
         board_msg.area3=""
         board_msg.area4=""
         board_msg.area5=""
         board_msg.area6=""
         board_msg.area7=""
         board_msg.area8=""
         board_msg.area9=""
         contours=red_detection(frame)
         for pic, contour in enumerate(contours):
                  area = cv2.contourArea(contour)
                  if(area > 800):
                         x, y, w, h = cv2.boundingRect(contour)
                         frame = cv2.rectangle(frame, (x, y),  
										(x + w, y + h), 
										(0, 0, 255), 8) 
                         for rect in rectangles.keys():
                              if (x>int(rectangles[rect]["x"])) and ((x+w)<(int(rectangles[rect]["x"])+int(rectangles[rect]["w"]))):
                                   if (y>int(rectangles[rect]["y"])) and ((y+h)<(int(rectangles[rect]["y"])+int(rectangles[rect]["h"]))):
                                        print("RED object inside "+str(rectangles[rect]["name"]))
                                        
                                        if str(rectangles[rect]["name"])=="A1":
                                             board_msg.area1="R"
                                        if str(rectangles[rect]["name"])=="A2":
                                             board_msg.area2="R"
                                        if str(rectangles[rect]["name"])=="A3":
                                             board_msg.area3="R"
                                        if str(rectangles[rect]["name"])=="A4":
                                             board_msg.area4="R"
                                        if str(rectangles[rect]["name"])=="A5":
                                             board_msg.area5="R"
                                        if str(rectangles[rect]["name"])=="A6":
                                             board_msg.area6="R"
                                        if str(rectangles[rect]["name"])=="A7":
                                             board_msg.area7="R"
                                        if str(rectangles[rect]["name"])=="A8":
                                             board_msg.area8="R"
                                        if str(rectangles[rect]["name"])=="A9":
                                             board_msg.area9="R"

         contours=blue_detection(frame)
         for pic, contour in enumerate(contours):
                  area = cv2.contourArea(contour)
                  if(area > 800):
                         x, y, w, h = cv2.boundingRect(contour)
                         frame = cv2.rectangle(frame, (x, y),  
										(x + w, y + h), 
										(255, 0, 0), 8) 
                         for rect in rectangles.keys():
                              if (x>int(rectangles[rect]["x"])) and ((x+w)<(int(rectangles[rect]["x"])+int(rectangles[rect]["w"]))):
                                   if (y>int(rectangles[rect]["y"])) and ((y+h)<(int(rectangles[rect]["y"])+int(rectangles[rect]["h"]))):
                                        print("BLUE object inside "+str(rectangles[rect]["name"]))
                                        
                                        if str(rectangles[rect]["name"])=="A1":
                                             board_msg.area1="B"
                                        if str(rectangles[rect]["name"])=="A2":
                                             board_msg.area2="B"
                                        if str(rectangles[rect]["name"])=="A3":
                                             board_msg.area3="B"
                                        if str(rectangles[rect]["name"])=="A4":
                                             board_msg.area4="B"
                                        if str(rectangles[rect]["name"])=="A5":
                                             board_msg.area5="B"
                                        if str(rectangles[rect]["name"])=="A6":
                                             board_msg.area6="B"
                                        if str(rectangles[rect]["name"])=="A7":
                                             board_msg.area7="B"
                                        if str(rectangles[rect]["name"])=="A8":
                                             board_msg.area8="B"
                                        if str(rectangles[rect]["name"])=="A9":
                                             board_msg.area9="B"
         board_pub.publish(board_msg)		
         cv2.imshow("Edges", frame) 
        
         if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        
    print("EXIT")  
    # Release the webcam and close the windows 
    cap.release() 
    cv2.destroyAllWindows()

    

if __name__ == "__main__": 
    
    main()




