from pid import PIDController
from detection import ColorAndContourDetector
from estimator import BallEstimator
from shot_counter import ShotCounter
from djitellopy import Tello
import cv2

PERIOD = 1 # ms

tello = Tello()
tello.connect()
# tello.takeoff()
tello.streamon()

leftRightPID = PIDController(0.1, 0, 0.0001, PERIOD / 1000)
upDownPID = PIDController(0.2, 0, 0, PERIOD / 1000)
forwardBackwardPID = PIDController(1, 0, 0, PERIOD / 1000)

detector = ColorAndContourDetector()
ball_estimator = BallEstimator()
shot_counter = ShotCounter()

while True:
    frame = tello.get_frame_read().frame
    ball = detector.detect(frame)
    if ball is not None:
        ball_estimator.update(ball, PERIOD / 1000)
    else:
        ball = ball_estimator.estimate(PERIOD / 1000)

    shot_counter.update(drone.get_height(), ball)
    
    leftRight = int(leftRightPID.next(ball.centroid[0] - 480))
    upDown = int(upDownPID.next(360 - ball.centroid[1]))
    forwardBackward = int(forwardBackwardPID.next(35 - ball.radius))
    tello.send_rc_control(leftRight, forwardBackward, upDown, 0)

    cv2.imshow("Tello Camera", frame)

    if cv2.waitKey(PERIOD) & 0xFF == ord('q'):
        break

tello.send_rc_control(0, 0, 0, 0)
tello.land()
tello.streamoff()