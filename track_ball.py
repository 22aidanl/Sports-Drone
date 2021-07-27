from pid import PIDController
from basketball import Basketball
from djitellopy import Tello
import cv2
import numpy as np

tello = Tello()
tello.connect()
tello.streamon()

while True:
    frame = tello.get_frame_read().frame
    if frame is not None:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        bballLower = np.array([4,200,150])
        bballUpper = np.array([14,255,255])
        mask = cv2.inRange(hsv, bballLower, bballUpper)
        hsv = cv2.bitwise_and(hsv, hsv, mask=mask)

        gray = cv2.split(hsv)[2]
        gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, np.ones((15, 15)))
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contours, -1, (0, 255, 0), thickness=5)

        bball = Basketball(contours)
        if hasattr(bball, "centroid"):
            cv2.circle(frame, bball.centroid, 5, (255, 0, 0), thickness=10)

        cv2.imshow("Tello Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

tello.streamoff()