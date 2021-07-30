from pid import PIDController
from detection import ColorAndContourDetector
from estimator import BallEstimator
from djitellopy import Tello
import cv2

PERIOD = 1 # ms

tello = Tello()
tello.connect()
tello.takeoff()
# tello.move("up", 50)
tello.streamon()

leftRightPID = PIDController(0.1, 0, 0.0001, PERIOD / 1000)
upDownPID = PIDController(0.2, 0, 0, 0.001, PERIOD / 1000)
forwardBackwardPID = PIDController(1, 0, 0, 0.001, PERIOD / 1000)

ball_estimator = BallEstimator()

while True:
    frame = tello.get_frame_read().frame
    if frame is not None:
        ball = ColorAndContourDetector.detect(frame)
        if ball.centroid is None:
            ball = ball_estimator.estimate(ball, PERIOD / 1000)
        else:
            ball_estimator.update(ball, PERIOD / 1000)
        
        leftRight = int(leftRightPID.next(ball.centroid[0] - 480))
        upDown = int(upDownPID.next(360 - ball.centroid[1]))
        # forwardBackward = int(forwardBackwardPID.next(35 - ball.radius))
        forwardBackward = int(forwardBackwardPID.next(10 - ball.radius))
        print(35 - ball.radius)
        tello.send_rc_control(leftRight, forwardBackward, upDown, 0)
        
        cv2.imshow("Tello Camera", frame)

        if cv2.waitKey(PERIOD) & 0xFF == ord('q'):
            break

tello.send_rc_control(0, 0, 0, 0)
tello.land()
tello.streamoff()