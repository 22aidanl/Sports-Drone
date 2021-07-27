import cv2
import os

# Coordinates to view the HSV values of
loc = (0, 0)

frame = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + "/1.jpg")
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
print(hsv[loc])

cv2.circle(frame, loc, 5, (0, 255, 0), thickness=2)
cv2.imshow("Frame", frame)
cv2.waitKey(0)