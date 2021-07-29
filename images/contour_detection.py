import cv2
import numpy as np
import os

frame = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + "/1.jpg")

# Convert to HSV and use color ranges for a basketball
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
bballLower = np.array([5,90,100])
bballUpper = np.array([30,255,255])
mask = cv2.inRange(hsv, bballLower, bballUpper)
hsv = cv2.bitwise_and(hsv, hsv, mask=mask)

# Use grayscale to find all contours and draw them
gray = cv2.split(hsv)[2]
gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, np.ones((15, 15)))
contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(frame, contours, -1, (0, 255, 0), thickness=5)
cv2.imshow("Frame", frame)
cv2.waitKey(0)
