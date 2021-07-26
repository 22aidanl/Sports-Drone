import cv2
import numpy as np
from djitellopy import tello

#my_drone = tello.Tello()
#my_drone.connect()
#my_drone.streamon()

while True:
    #frame = my_drone.get_frame_read().frame
    image = '1.jpg'
    frame = cv2.imread(image, 1)
    img = frame.copy()

    if frame is not None:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (15, 15), cv2.BORDER_DEFAULT)
        gray = cv2.medianBlur(gray, 5)
        cv2.imshow('Frame', img)
        cv2.waitKey(1)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 120, param1=100, param2=30, minRadius=0,
                                   maxRadius=250) ##CHANGE THESE VALUES AS NEEDED##
        circles = np.uint16(np.around(circles))
        #print(circles)
        #print(circles.shape)

    num = 1
    for i in circles[0,:]:
        cv2.circle(img, i[0], i[1], i[2], (0, 200, 255), 5) ##CHANGE THESE VALUES AS NEEDED##
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 10) ##CHANGE THESE VALUES AS NEEDED##
        num += 1

    #cv2.imshow('Frame', img)
    #cv2.waitKey(1)
    cv2.imwrite("Image", img)

