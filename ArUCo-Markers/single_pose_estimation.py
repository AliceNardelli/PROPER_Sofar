'''
Sample Command:-
python3 single_pose_estimation.py  --type DICT_5X5_100 --K_Matrix calibration_matrix.npy --D_Coeff distortion_coefficients.npy
'''
import numpy as np
from utils import ARUCO_DICT, aruco_display
import argparse
import cv2
import sys
from scipy.spatial.transform import Rotation as R
from flask import Flask, request, jsonify
import os
import shutil
import subprocess
import json
import time
import numpy as np
import math

data={
    "x":0,
    "y":0,
    "z":0,
    "yaw":0,
    "roll":0,
    "pitch":0
}

data_aruco={
    "x":0,
    "y":0,
    "z":0,
    "yaw":0,
    "roll":0,
    "pitch":0
}

T_0_13=[[0,0,-1,1.8],
        [-1,0,0,0],
        [0,1,0,0],
        [0,0,0,1]]

R_0_13=[[0,1,0],
        [0,0,-1],
        [-1,0,0]]

T_0_24=[[0,1,0,-1.8],
        [0,0,1,0],
        [1,0,0,1],
        [0,0,0,1]]

# --- 90 deg rotation matrix camera around the x axis
R_x = np.zeros((3, 3), dtype=np.float32)
R_x[0, 0] = 1.0
R_x[1, 2] = -1.0
R_x[2, 1] = 1.0

# --- 90 deg rotation matrix camera around the z axis
R_z = np.zeros((3, 3), dtype=np.float32)
R_z[1, 0] = 1.0
R_z[0, 1] = -1.0
R_z[2, 2] = 1.0

app = Flask(__name__)

def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians

def pose_esitmation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()


    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters,
        cameraMatrix=matrix_coefficients,
        distCoeff=distortion_coefficients)
    
    
    if len(corners) > 0:
        print("idss"+str(ids))
        for i in range(0, len(ids)):
                # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
                ret = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.2, matrix_coefficients, distortion_coefficients)
                rvec, tvec = ret[0][0,0,:], ret[1][0,0,:]
                #Draw a square around the markers
                cv2.aruco.drawDetectedMarkers(frame, corners) 
                # Draw Axis
                cv2.aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)
                
                print("position marker wrt camera frame defined by Aruco", tvec)
                
                x1 = np.dot(tvec, R_x)
                tvec_2 = np.dot(x1, R_z)

                print("position maker wrt camera frame defined by Naoqi", tvec_2)

                # Compute distance between Pepper and the detected marker
                distance = math.sqrt((tvec_2[0] * tvec_2[0]) + (tvec_2[1] * tvec_2[1]))
                print("distance marker", distance)
                print("Rotation",rvec)
                # -- Obtain the rotation matrix Marker -> camera
                R_cm = np.matrix(cv2.Rodrigues(rvec)[0])
                R_mc = R_cm.T
                print("Rotation Matrix marker->Camera", R_mc)
                r = R.from_matrix(R_cm)
                yaw, pitch, roll = r.as_euler('zxy', degrees=False)
                print("yaw",yaw)
                """
                # -- Obtain the transformation matrix marker -> camera
                T_cm = np.zeros((4, 4), dtype=float)
                T_cm[0:3, 0:3] = R_cm
                T_cm[0:3, 3] = tvec
                T_cm[3, 3] = 1
                
                #compute the transformation matrix of the robot wrt the world
                if 13 in ids:
                    tvecn=np.concatenate((tvec,np.array([1.0])),axis=0)
                    tsl=np.dot(T_0_13,tvecn)
                elif 24 in ids:
                    tvecn=np.concatenate((tvec,np.array([1.0])),axis=0)
                    print(tvecn)
                    tsl=np.dot(T_0_24,tvecn)
                else:
                     break
                
                X_now=tsl[0]
                Y_now=tsl[1]
                print("---------")
                print(X_now,Y_now,yaw)
                print("---------")
                """
                return "True", tvec_2[0], tvec_2[1], yaw , ids[0][0]  
    print("Aruco not found")
    return "False", 0,0,0,0




@app.route ('/odom_offset', methods = ['PUT'] )
def get_params():
    #get actual odometry
    updated_data = request.get_json()
    data.update(updated_data)
    #detect aruco in the last computed image
    success="" 
    X_now=0 
    Y_now=0 
    yaw=0
    id=0
    for i in range(5):
        file="/home/alice/images/image"+str(i)+".png"
        #file="/home/alice/images/image_.png"
        image = cv2.imread(file)
        h,w,_ = image.shape
        width=600
        height = int(width*(h/w))
        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)
        aruco_dict_type = ARUCO_DICT["DICT_5X5_100"]
        calibration_matrix_path = "pepper2_calibration_matrix.npy"
        distortion_coefficients_path = "pepper2_distortion_coefficients.npy"
        k = np.load(calibration_matrix_path)
        d = np.load(distortion_coefficients_path)
        success, X_now, Y_now, yaw,id = pose_esitmation(image, aruco_dict_type, k, d)
        if success=="True":
             break
    if success=="True":
        #update the offset
        data_aruco["success"]="True"
        data_aruco["x"]=str(X_now)
        data_aruco["y"]=str(Y_now)
        data_aruco["yaw"]=str(yaw)
        data_aruco["id"]=str(id)
    else:
        data_aruco["success"]="False"
        data_aruco["x"]=str(0)
        data_aruco["y"]=str(0)
        data_aruco["yaw"]=str(-3.14)
        data_aruco["id"]=str(0)
    return jsonify(data_aruco)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50010, debug=True)



    
 
