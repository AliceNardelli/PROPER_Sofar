import cv2
from datetime import datetime
from imutils.video import VideoStream
import time

vs = VideoStream(src=0).start()
time.sleep(2.0)
c=0
while(True):
    frame = vs.read()

    cv2.imshow('frame',frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('c'):
        cv2.imwrite("/home/alice/images/cal/im_"+str(c)+".png",frame)
        c+=1
vs.stop()
cv2.destroyAllWindows()