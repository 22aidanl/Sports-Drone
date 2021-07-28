from pid import PIDController
from basketball import Basketball
from djitellopy import Tello
import cv2
import numpy as np

tello = Tello()
tello.connect()

tello.takeoff()
tello.move("up", 50)
tello.streamon()
leftRightPID = PIDController(0.1, 0, 0, 0.001)
upDownPID = PIDController(0.2, 0, 0, 0.001)

while True:
    frame = tello.get_frame_read().frame
    if frame is not None:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        bballLower = np.array([4,150,100])
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
            leftRight = int(leftRightPID.next(bball.centroid[0] - 480))
            upDown = int(upDownPID.next(360 - bball.centroid[1]))
            tello.send_rc_control(leftRight, 0, upDown, 0)
        else:
            tello.send_rc_control(0, 0, 0, 0)
        cv2.imshow("Tello Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
tello.send_rc_control(0, 0, 0, 0)
tello.land()
tello.streamoff()