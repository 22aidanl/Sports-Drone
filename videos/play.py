import cv2
import numpy as np
import os

cap = cv2.VideoCapture(os.path.dirname(os.path.realpath(__file__)) + "/1.avi")

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Recorded Video", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()