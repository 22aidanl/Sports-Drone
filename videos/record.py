import cv2
from djitellopy import Tello
import os

tello = Tello()
tello.connect()
tello.streamon()
writer = cv2.VideoWriter(os.path.dirname(os.path.realpath(__file__)) + "/1.avi", cv2.VideoWriter_fourcc(*'XVID'), 30, (960,720))

while True:

    frame = tello.get_frame_read().frame
    cv2.imshow("Recording", frame)
    writer.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


writer.release()
tello.streamoff()
