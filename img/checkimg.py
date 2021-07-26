import cv2
import numpy as np
import os

pic = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + "/3.jpg")
pic = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)

bballLower = np.array([0,50,0])
bballUpper = np.array([12,255,255])
mask = cv2.inRange(pic, bballLower, bballUpper)
pic = cv2.bitwise_and(pic, pic, mask=mask)
pic = cv2.cvtColor(pic, cv2.COLOR_HSV2BGR)

gray = cv2.split(pic)[2]
gray = cv2.medianBlur(gray, 5)
rows = gray.shape[0]
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 2,
                                param1=100, param2=30,
                                minRadius=20, maxRadius=200)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        center = (i[0], i[1])
        radius = i[2]
        cv2.circle(pic, center, radius, (255, 0, 255), 3)

print(circles)
cv2.imshow("Pic", pic)
cv2.waitKey(0)