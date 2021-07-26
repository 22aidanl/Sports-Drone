from djitellopy import Tello
import cv2
import numpy as np

tello = Tello()
tello.connect()
tello.streamon()

while True:
    frame = tello.get_frame_read().frame
    if frame is not None:
        # bballLower = np.array([0,20,70])
        # bballUpper = np.array([30,50,110])
        # mask = cv2.inRange(frame, bballLower, bballUpper)
        # frame = cv2.bitwise_and(frame, frame, mask=mask)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        rows = gray.shape[0]
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                                param1=100, param2=30,
                                minRadius=140, maxRadius=170)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                # cv2.circle(frame, center, 1, (0, 100, 100), 3)
                # circle outline
                radius = i[2]
                # cv2.circle(frame, center, radius, (255, 0, 255), 3)

        cv2.imshow("Tello Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("/Users/aidanlincke/Documents/Beaver Works/Sports-Drone/test2.jpg", frame)
            break

tello.streamoff()