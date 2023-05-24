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

def pose_esitmation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients, goal):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters,
        cameraMatrix=matrix_coefficients,
        distCoeff=distortion_coefficients)
    
    
    if len(corners) > 0:
        print("idss"+str(ids))
        for i in range(0, len(ids)):
            if goal in ids:
                # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.07, matrix_coefficients,
                                                                        distortion_coefficients)
                # Draw a square around the markers
                cv2.aruco.drawDetectedMarkers(frame, corners) 

                # Draw Axis
                cv2.aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)
                
                rot_mat, _=cv2.Rodrigues(rvec[0][0])
                l1=np.append(rot_mat[0],[tvec[0][0][0]])
                l2=np.append(rot_mat[1],[tvec[0][0][1]])
                l3=np.append(rot_mat[2],[tvec[0][0][2]])
                l4=np.array([0,0,0,1])
                tr=np.concatenate(([l1],[l2],[l3],[l4]),axis=0)               
                inv_tr=np.linalg.inv(tr)

                print(inv_tr)
                x=inv_tr[0][3]
                y=inv_tr[1][3]
                z=inv_tr[2][3]
                tnsl=[x,y,z]
                inv_rot_mat=np.linalg.inv(rot_mat)
                r = R.from_matrix(inv_rot_mat)
                quat=r.as_quat()
                euler=euler_from_quaternion(quat[0],quat[1],quat[2],quat[3])
                return "True", frame, euler, tnsl
            else:
                print("Goal aruco not found")
                return "False", [], [], []
                
    print("Aruco not found")
    return "False", [], [], []

if __name__ == '__main__':
    path="/home/alice/images/lato2/"
    file=path+"Image_13_plus20.png"
    image = cv2.imread(file)
    h,w,_ = image.shape
    width=600
    height = int(width*(h/w))
    image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)
    aruco_dict_type = ARUCO_DICT["DICT_5X5_100"]
    calibration_matrix_path = "/home/alice/catkin_ws/src/PROPER_Sofar/ArUCo-Markers/pepper_calibration_matrix.npy"
    distortion_coefficients_path = "/home/alice/catkin_ws/src/PROPER_Sofar/ArUCo-Markers/pepper_distortion_coefficients.npy"
    k = np.load(calibration_matrix_path)
    d = np.load(distortion_coefficients_path)
    success, output, euler, transl = pose_esitmation(image, aruco_dict_type, k, d,13)
    if success=="True":
        cv2.imwrite("/home/alice/images/lato2/output_13_plus20.png",output)
        res={
            "success":success,
            "rpy":str(euler),
            "translation":str(transl)
        }
    else:
        res={
            "success":success,
            "rpy":[],
            "translation":[]
        }
    print(res)    
   