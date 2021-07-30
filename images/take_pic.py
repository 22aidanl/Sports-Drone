from djitellopy import Tello
import cv2
import os

tello = Tello()
tello.connect()
tello.streamon()

while True:
    frame = tello.get_frame_read().frame
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite(os.path.dirname(os.path.realpath(__file__)) + "/3.jpg", frame)
        break

tello.streamoff()