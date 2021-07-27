import cv2
import numpy as np
from djitellopy import tello

my_drone = tello.Tello()
my_drone.connect()
my_drone.streamon()

while True:
    frame = my_drone.get_frame_read().frame
    if frame is not None:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        new = cv2.medianBlur(gray, 5)
        #newimg = cv2.cvtColor(new, cv2.COLOR_GRAY2BGR)

        circles = cv2.HoughCircles(new, cv2.HOUGH_GRADIENT, 1, 400, param1=100, param2=30, minRadius=0, maxRadius=250)
        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 3)
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 10)

        cv2.imshow('Frame', frame)
        cv2.waitKey(int(1000/16))
