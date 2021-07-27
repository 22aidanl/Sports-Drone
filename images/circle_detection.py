import cv2
import numpy as np
from djitellopy import tello
import os

#my_drone = tello.Tello()
#my_drone.connect()
#my_drone.streamon()

#frame = my_drone.get_frame_read().frame
frame = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + '/1.jpg')
#img = frame.copy()

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#new = cv2.GaussianBlur(gray, (15, 15), cv2.BORDER_DEFAULT)
new = cv2.medianBlur(gray, 5)

newimg = cv2.cvtColor(new, cv2.COLOR_GRAY2BGR)
#cv2.imshow('Frame', img)
#cv2.waitKey(1)
##CHANGE THE BELOW VALUES AS NEEDED##
circles = cv2.HoughCircles(new, cv2.HOUGH_GRADIENT, 1, 360, param1=100, param2=30, minRadius=0, maxRadius=250)
circles = np.uint16(np.around(circles))
        #print(circles)
        #print(circles.shape)

for i in circles[0, :]:
    cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 10) ##CHANGE THESE VALUES AS NEEDED##
    cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 10) ##CHANGE THESE VALUES AS NEEDED##

cv2.imshow('Frame', frame)
#cv2.imwrite("Circles.jpg", frame)
cv2.waitKey(0)
