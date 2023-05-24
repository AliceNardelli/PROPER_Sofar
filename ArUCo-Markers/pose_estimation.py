'''
Sample Usage:-
python pose_estimation.py --K_Matrix calibration_matrix.npy --D_Coeff distortion_coefficients.npy --type DICT_5X5_100
'''


import numpy as np
import cv2
import sys
from utils import ARUCO_DICT
import argparse
import time


def pose_esitmation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):
    '''
    frame - Frame from the video stream
    matrix_coefficients - Intrinsic matrix of the calibrated camera
    distortion_coefficients - Distortion coefficients associated with your camera

    return:-
    frame - The frame with the axis drawn on it
    '''
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()


    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters,
        cameraMatrix=matrix_coefficients,
        distCoeff=distortion_coefficients)

        # If markers are detected
    if len(corners) > 0:
        for i in range(0, len(ids)):
            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.08, matrix_coefficients,
                                                                       distortion_coefficients)
            # Draw a square around the markers
            cv2.aruco.drawDetectedMarkers(frame, corners) 

            # Draw Axis
            cv2.aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)
            print(rvec,tvec)

    return frame

if __name__ == '__main__':

    aruco_dict_type = ARUCO_DICT["DICT_5X5_100"]
    calibration_matrix_path = "/home/alice/catkin_ws/src/PROPER_Sofar/ArUCo-Markers/new_calibration_matrix.npy"
    distortion_coefficients_path = "/home/alice/catkin_ws/src/PROPER_Sofar/ArUCo-Markers/new_distortion_coefficients.npy"
    
    k = np.load(calibration_matrix_path)
    d = np.load(distortion_coefficients_path)

    video = cv2.VideoCapture(0)
    time.sleep(2.0)
    c=0
    while True:
        ret, frame = video.read()

        if not ret:
            break

       # cv2.imwrite("/home/alice/images/cal/im_"+str(c)+".png",frame)
        c+=1
        output = pose_esitmation(frame, aruco_dict_type, k, d)

        cv2.imshow('Estimated Pose', output)
        
        key = cv2.waitKey(1) 
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
