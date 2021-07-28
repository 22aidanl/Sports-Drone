from pid import PIDController
from detection import ColorAndContourDetector
from djitellopy import Tello
import cv2
import numpy as np

tello = Tello()
tello.connect()
tello.takeoff()
# tello.move("up", 50)
tello.streamon()
leftRightPID = PIDController(0.1, 0, 0.0001, 0.001)
upDownPID = PIDController(0.2, 0, 0, 0.001)
forwardBackwardPID = PIDController(0.06, 0, 0.0001, 0.001)

initialArea = None

detector = ColorAndContourDetector()

while True:
    frame = tello.get_frame_read().frame
    if frame is not None:
        ball = detector.detect(frame)
        if ball.centroid:
        
            cv2.circle(frame, ball.centroid, 5, (255, 0, 0), thickness=10)
            leftRight = int(leftRightPID.next(ball.centroid[0] - 480))
            upDown = int(upDownPID.next(360 - ball.centroid[1]))
            if initialArea is None:
                initialArea = ball.area
                forwardBackward = 0
            else:
                forwardBackward = int(forwardBackwardPID.next(initialArea - ball.area))
            tello.send_rc_control(leftRight, forwardBackward, upDown, 0)
            
        # Uncomment for drone to stop when ball is out of frame
        # else:
            # tello.send_rc_control(0, 0, 0, 0)
        cv2.imshow("Tello Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

tello.send_rc_control(0, 0, 0, 0)
tello.land()
tello.streamoff()