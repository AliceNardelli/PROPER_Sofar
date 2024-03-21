
# import the opencv library 
import cv2 
#from pygaze import PyGaze, PyGazeRenderer 
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
bridge = CvBridge()

rospy.init_node('talker', anonymous=True)

# define a video capture object 
vid = cv2.VideoCapture(0) 
#pg = PyGaze()
#pgren = PyGazeRenderer()
pub = rospy.Publisher('chatter', Image, queue_size=10)
rate = rospy.Rate(10)    

while not rospy.is_shutdown(): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
    im=Image()
    ros_image=bridge.cv2_to_imgmsg(frame, encoding="passthrough")
    print(type(ros_image))
    pub.publish(ros_image)
    
    """
    gaze_result = pg.predict(frame)
    for face in gaze_result:
        print(f"Face bounding box: {face.bbox}")
        pitch, yaw, roll = face.get_head_angles()
        g_pitch, g_yaw = face.get_gaze_angles()
        print(f"Face angles: pitch={pitch}, yaw={yaw}, roll={roll}.")
        print(f"Distance to camera: {face.distance}")
        print(f"Gaze angles: pitch={g_pitch}, yaw={g_yaw}")
        print(f"Gaze vector: {face.gaze_vector}")
        print(f"Looking at camera: {pg.look_at_camera(face)}")
	
        img = pgren.render(frame, face, draw_face_bbox=True, draw_face_landmarks=False, draw_3dface_model=False,draw_head_pose=False, draw_gaze_vector=True)
    """
    cv2.imshow("Face",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
vid.release() 
cv2.destroyAllWindows() 