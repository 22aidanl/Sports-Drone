from pid import PIDController
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

        bballLower = np.array([0,50,0])
        bballUpper = np.array([12,255,255])
        mask = cv2.inRange(hsv, bballLower, bballUpper)
        hsv = cv2.bitwise_and(hsv, hsv, mask=mask)
        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        gray = cv2.split(frame)[2]
        gray = cv2.medianBlur(gray, 5)
        rows = gray.shape[0]
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 2,
                                        param1=100, param2=30,
                                        minRadius=20, maxRadius=170)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                radius = i[2]
                cv2.circle(frame, center, radius, (255, 0, 255), 3)

        cv2.imshow("Tello Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

tello.streamoff()