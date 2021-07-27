import cv2
import numpy as np
import os


frame = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + '/1.jpg')
#img = frame.copy()

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
new = cv2.medianBlur(gray, 5)
newimg = cv2.cvtColor(new, cv2.COLOR_GRAY2BGR)

##CHANGE THE BELOW VALUES AS NEEDED##
#for second image# circles = cv2.HoughCircles(new, cv2.HOUGH_GRADIENT, 1, 800, param1=10, param2=30, minRadius=0, maxRadius=250)
circles = cv2.HoughCircles(new, cv2.HOUGH_GRADIENT, 1, 360, param1=100, param2=30, minRadius=0, maxRadius=250)
circles = np.uint16(np.around(circles))

for i in circles[0, :]:
    cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 3)
    cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 10)

cv2.imshow('Frame', frame)
cv2.waitKey(0)
