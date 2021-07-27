from __future__ import division
import cv2
import numpy as np
import imutils
import os
from djitellopy import tello
import os


#connect to tello
me = tello.Tello()
me.connect()
me.streamon()
print(me.get_battery())

frame = me.get_frame_read().frame
frame = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + '/1.jpg')
img = frame.copy()
frame = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + "/1.jpg")

while True:


    # Convert to HSV, use color ranges for a basketball, and convert back to BGR
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    bballLower = np.array([0, 150, 150])
    bballUpper = np.array([15, 255, 255])
    mask = cv2.inRange(hsv, bballLower, bballUpper)
    hsv = cv2.bitwise_and(hsv, hsv, mask=mask)

    # Use grayscale to find all contours and draw them
    gray = cv2.split(hsv)[2]
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, np.ones((15, 15)))
    cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:

        area = cv2.contourArea(c)

        cv2.drawContours(frame, cnts, -1, (0, 255, 0), thickness=5)

        M = cv2.moments(c)

        cx = int(M["m10"]/ M["m00"])
        cy = int(M["m01"] / M["m00"])

        cv2.circle(frame, (cx,cy),2,(0,0,255), 10)
        cv2.putText(frame, "Centroid", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,0), 1)

        cv2.imshow("frame", frame)

        print("area is ...", area)
        print("centroid is at...", cx,cy)




    img = me.get_frame_read().frame
    cv2.imshow("Image", img)
    cv2.waitKey(1)

