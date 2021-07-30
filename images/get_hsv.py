import cv2
import os

# Coordinates to view the HSV values of
x = 410
y = 449

frame = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + "/3.jpg")
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

hue, sat, val = hsv[(y, x)]

hue *= (360 / 179)
sat *= (100 / 255)
val *= (100 / 255)
print(hue, sat, val)


cv2.circle(frame, (x, y), 5, (0, 255, 0), thickness=2)
cv2.imshow("Frame", frame)
cv2.waitKey(0)