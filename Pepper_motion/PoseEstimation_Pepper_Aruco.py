"""
In the following code, the pose estimation of the robot wrt world frame is computed, by using Aruco Marker.

What we have:
1) the position and the orientation of the world frame (x_w; y_w, theta_w);
2) position of the Aruco marker wrt world frame;
3) the camera matrix and dist coeff, because the calibration of the camera is done with the GUI. They have been saved into a file .npy.

What the code does:
1) detection of the aruco marker -> ('PoseEstimation' function);
2) pose estimation of the aruco marker with respect to the camera frame, which is defined according to the Aruco library rules (where the normal of the camera is z axis) -> ('PoseEstimation' function);
3) get the coordinates of the aruco pose wrt the camera frame defined according to the NAOqi rules (where the normal of the camera is x axis) -> ('PoseEstimation' function);
4) get the transformation matrix between the camera frame and the robot frame (getTransform()) -> ('TransformationRobotCameraFrame' function);
5) Finally get the position of the marker wrt robot frame -> ('PoseEstimation' function);
6) After defining the pose and orientation of the world frame and knowing the position of the marker wrt world frame, it gets the position of the robot wrt world frame -> ('ComputeWorldPepperPosition' function).

"""

import qi
import argparse
import sys
import time
import cv2
import numpy as np
import math
import vision_definitions
import glob
import threading
import Queue
from EKF import *

DetectMarker = False


# class for storing infos about the markers
class Marker:
    def __init__(self, ID, x, y, theta):
        # ID of the marker
        self.ID = ID
        # x position in the world frame of the marker
        self.x = x
        # y position in the world frame of the marker
        self.y = y
        # theta angulation in the world frame of the marker
        self.theta = theta


# store information about the markers
markers = [Marker(13, 1.8, 0.0, 3)]


# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6


# Calculates rotation matrix to euler angles
def rotationMatrixToEulerAngles(R):
    # assert (isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])


# Calculate euler to quaternion
def eulerToQuaternion(yaw, pitch, roll):

    X = np.array([np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2)]) - \
        np.array([np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)])
    Y = np.array([np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)]) + \
        np.array([np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)])
    Z = np.array([np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)]) - \
        np.array([np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)])
    W = np.array([np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2)]) + \
        np.array([np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)])

    return X, Y, Z, W


def Rx(theta):
    return np.matrix([[1, 0, 0],
                      [0, math.cos(theta), -math.sin(theta)],
                      [0, math.sin(theta), math.cos(theta)]])


def Ry(theta):
    return np.matrix([[math.cos(theta), 0, math.sin(theta)],
                      [0, 1, 0],
                      [-math.sin(theta), 0, math.cos(theta)]])


def Rz(theta):
    return np.matrix([[math.cos(theta), -math.sin(theta), 0],
                      [math.sin(theta), math.cos(theta), 0],
                      [0, 0, 1]])


def PoseEstimation(session, mtx, dist, robotPose_w):
 
    # -- DEFINE THE NEEDED ROTATION MATRICES
    # --- 180 deg rotation matrix camera around the x axis
    R_flip = np.zeros((3, 3), dtype=np.float32)
    R_flip[0, 0] = 1.0
    R_flip[1, 1] = -1.0
    R_flip[2, 2] = -1.0

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

    try:
        # get the service ALVideoDevice.
        video_service = session.service("ALVideoDevice")
        # cameraID = 0 # Top Camera
        cameraID = 1  # Bottom Camera
        # cameraID = 2 # Depth Camera
        # cameraID = 3 # Stereo Camera
        resolution = vision_definitions.kQVGA # 320 * 240
        colorSpace = vision_definitions.kBGRColorSpace

        fps = 5
        videoClient = video_service.subscribe("python_client", resolution, colorSpace, fps)

        print "Client name: ", videoClient
        if videoClient != '':
            video_service.setParam(vision_definitions.kCameraSelectID, cameraID)
            userWantsToExit = False

            while not userWantsToExit:
                t0 = time.time()
                pepperImage = video_service.getImageRemote(videoClient)
                t1 = time.time()
                time_elapsed = float(t1 -t0)
                if time_elapsed > 0.0:
                    fps = 1/time_elapsed

                if pepperImage is not None:
                    # Get the image size and pixel array.
                    imageWidth = pepperImage[0]
                    imageHeight = pepperImage[1]
                    img_array = pepperImage[6]

                    # define aruco dictionary
                    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
                    # arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_100)
                    arucoParams = cv2.aruco.DetectorParameters_create()

                    img_str = str(bytearray(img_array))
                    video_service.releaseImage(videoClient)

                    # # Reshape array to show the image
                    # depth : np.uint16
                    # camera normale: np.uint8
                    nparr = np.fromstring(img_str, np.uint8)
                    frame = nparr.reshape(((imageHeight, imageWidth, 3))).astype(np.uint8)

                    scale_percent = 200 # percent of original size
                    width = int(frame.shape[1] * scale_percent / 100)
                    height = int(frame.shape[0] * scale_percent / 100)
                    dim = (width, height)

                    # # resize image
                    # img_np = cv2.resize(img_np, dim, interpolation = cv2.INTER_AREA)
                    # frame = imutils.resize(img_np, width=1000)

                    # DETECTION ARUCO MARKER
                    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

                    # if a marker is found:
                    if np.all(ids is not None):
                        DetectMarker = True
                        zipped = zip(ids, corners)
                        ids, corners = zip(*(sorted(zipped)))

                        print "ID: ", ids[0][0]

                        for index, marker in enumerate(markers):
                            if marker.ID == ids[0][0]:
                                x_aruco_w = marker.x
                                y_aruco_w = marker.y
                                theta_aruco_w = marker.theta

                        # ESTIMATION POSE MARKER
                        for i in range(0, len(ids)):

                            # the input are the corner of the estimated marker, the length size (in meter), the camera
                            # matrix and the dist coeff
                            ret = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.2, mtx, dist)

                            rvec, tvec = ret[0][0,0,:], ret[1][0,0,:]

                            print "position marker wrt camera frame defined by Aruco", tvec

                            """
                            NOTA: 
                            the same camera in the same orientation have different reference frame between aruco and naoqi: 
                            The camera reference frame  defined by Aruco is rotated about x axis of 90 deg and rotated 
                            about z axis of 90 de as well.
                            
                            Then we need to define the coordinate of the marker (that we have wrt camera frame defined 
                            according to the Aruco rules) wrt the camera frame defined according to the Naoqi rules. 
                            
                            As stated, the position of the marker (tvec) must be rotated about x axis (90 deg) and then 
                            about z axis (90 deg). 
                            """
                            x1 = np.dot(tvec, R_x)
                            tvec_2 = np.dot(x1, R_z)

                            print "position maker wrt camera frame defined by Naoqi", tvec_2

                            # Compute distance between Pepper and the detected marker
                            distance = math.sqrt((tvec_2[0] * tvec_2[0]) + (tvec_2[1] * tvec_2[1]))
                            print "distance marker", distance

                            cv2.aruco.drawDetectedMarkers(frame, corners)
                            cv2.aruco.drawAxis(frame, mtx, dist, rvec, tvec, 0.1)

                            # -- Obtain the rotation matrix Marker -> camera
                            R_cm = np.matrix(cv2.Rodrigues(rvec)[0])
                            R_mc = R_cm.T
                            print "Rotation Matrix marker->Camera", R_mc

                            # -- Obtain the transformation matrix marker -> camera
                            T_mc = np.zeros((4, 4), dtype=float)
                            T_mc[0:3, 0:3] = R_mc
                            T_mc[0:3, 3] = tvec_2
                            T_mc[3, 3] = 1
                            print "Transformation Matrix marker -> Camera", T_mc

                            # -- Get the attitude in terms of euler 321 (Needs to be flipped first)
                            roll_marker, pitch_marker, yaw_marker = rotationMatrixToEulerAngles(R_flip * R_mc)
                            print "euler angles of the marker in the camera frame", roll_marker, pitch_marker, yaw_marker

                            # -- Obtain the Transformation Matrix camera -> robot
                            T_cr, yaw_camera = TransformationRobotCameraFrame(session)

                            # -- Obtain the Transformation Matrix marker -> robot
                            T_mr = np.dot(T_cr, T_mc)
                            print "transformation Matrix Marker -> Robot", T_mr

                            # -- Obtain the rotation matrix marker -> robot
                            R_mr = T_mr[0:3, 0:3]
                            # -- Obtain the position of the marker wrt robot frame
                            position_marker_r = T_mr[0:3, 3]
                            print "position Marker in the robot frame", position_marker_r

                            # -- Compute the world position of the robot
                            x_robot_w, y_robot_w, theta_robot_w = ComputeWorldPepperPosition(pitch_marker, yaw_camera,
                                                                                             position_marker_r,
                                                                                             x_aruco_w, y_aruco_w,
                                                                                             theta_aruco_w)
                            print "position Robot in the world frame", x_robot_w, y_robot_w, theta_robot_w
                            robotpose = np.array([[x_robot_w], [y_robot_w], [theta_robot_w]])
                            robotPose_w.put(robotpose)

                            # if the marker has a distance less than 1.5 mt, then it does not take into account for
                            # the localization
                            if distance < 1.7:
                                robotPose_w.put(robotpose)
                                time.sleep(1)
                            else:
                                robotpose = np.array([[0], [0], [0]])
                                robotPose_w.put(robotpose)
                                time.sleep(1)
                    else:
                        robotpose = np.array([[0], [0], [0]])
                        robotPose_w.put(robotpose)
                        time.sleep(1)

                    # Write FPS on the screen
                    # cv2.putText(frame, str(fps)+" FPS", (5, 15), cv2.FONT_HERSHEY_SIMPLEX , 0.5, (20, 200, 15),
                    # 2, cv2.LINE_AA) # Write FPS on image

                    # # Show the image with cv2
                    cv2.imshow("Pepper camera", frame)
                    key = cv2.waitKey(1)
                    # If user press Esc, exit from the loop
                    if key == 27:
                        userWantsToExit = False
            # Unsubscribe from the video service
            video_service.unsubscribe(videoClient)

        else:
            print("Video client not found.")
    except KeyboardInterrupt:
        # Unsubscribe from the video service
        video_service.unsubscribe(videoClient)
        sys.exit(1)


def ComputeWorldPepperPosition(pitch_marker, yaw_camera, position_marker_r, x_aruco_w, y_aruco_w, theta_aruco_w):
    """

    Considerations:
    1) The world frame has been defined [x, y, theta];
    2) Aruco marker has been placed in the environment and the world position of this is known ( x_Aruco_w, y_Aruco_w,
    theta_Aruco_w);
    3) the orientation of the marker wrt camera frame is known: pitch_marker;
    4) the orientation of the camera wrt robot frame pepper is known: yaw_camera.

    Aim:
    Get the position of the robot wrt world frame.

    """
    print "pitch_marker", pitch_marker
    print "yaw_camera", yaw_camera

    theta_robot_w = -(pitch_marker + yaw_camera) - math.fabs(theta_aruco_w)

    x_aruco_p = position_marker_r[0]
    y_aruco_p = position_marker_r[1]

    x_robot_w = x_aruco_w - (x_aruco_p * math.cos(theta_robot_w) - y_aruco_p * math.sin(theta_robot_w))
    y_robot_w = y_aruco_w + (- x_aruco_p * math.sin(theta_robot_w) - y_aruco_p * math.cos(theta_robot_w))

    return x_robot_w, y_robot_w, theta_robot_w


def TransformationRobotCameraFrame(session):
    """
    Function to get the position and the orientation of the camera frame wrt robot frame according to NAoqi rules.
    """
    motion_service  = session.service("ALMotion")
    chainName = "CameraBottom"
    # -- Get current camera position in Robot Space
    # ALMotionproxy:getTransform(chainName, frame (0=torso; 1=world; 2=robot), usesensorvalues)

    transform = motion_service.getTransform(chainName, 2, True)

    # -- Obtain Transformation Matrix camera -> robot
    T_rc = np.reshape(transform, (4, 4))

    # -- Get Rotation Matrix camera -> robot
    R_cr = T_rc[0:3, 0:3]
    print "Rotation Matrix Camera -> Robot", R_cr

    # -- Get Position Camera -> robot
    position_camera = T_rc[0:3, 3]
    print "Position camera wrt Robot", position_camera

    # -- Get the attitude
    roll_camera, pitch_camera, yaw_camera = rotationMatrixToEulerAngles(R_cr)
    print "euler angles of the camera frame wrt robot frame", roll_camera, pitch_camera, yaw_camera

    return T_rc, yaw_camera


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="130.251.13.123",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    # awake pepper
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    # motion_service.wakeUp()
    posture_service.goToPosture("StandInit", 0.5)
    # motion_service.setAngles(["HeadPitch", "HeadYaw"], [0., 0.0], 0.2)
    # motion_service.rest()

    # initialization of the queue
    robotPose_w = Queue.Queue()
    mtx = np.load('CameraMatrix.npy')
    dist = np.load('DistCoeff.npy')

    print "matrix", mtx
    print "coeff", dist
    PoseEstimation(session, mtx, dist, robotPose_w)


