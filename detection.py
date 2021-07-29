from abc import ABC, abstractmethod
import cv2
import os
import numpy as np

class Ball:
    def __init__(self, centroid, radius, detection_method):
        self.centroid = centroid
        self.radius = radius
        self.detection_method = detection_method
    
    def __str__(self):
        return f"Basketball {{ centroid: {self.centroid}, radius: {self.radius} }} (detected with {self.detection_method}"

class BallDetector(ABC):
    @abstractmethod
    def detect(frame) -> Ball:
        pass

class ColorAndContourDetector(BallDetector):
    def detect(frame) -> Ball:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        bballLower = np.array([4,150,50])
        bballUpper = np.array([14,255,255])
        mask = cv2.inRange(hsv, bballLower, bballUpper)
        hsv = cv2.bitwise_and(hsv, hsv, mask=mask)

        gray = cv2.split(hsv)[2]
        gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, np.ones((15, 15)))
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largeContours = []
        xs = []
        ys = []
        totalArea = 0        

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 750:
                continue
            largeContours.append(contour)
            totalArea += area

            M = cv2.moments(contour)
            if M["m00"] != 0:
                centerX = int(M["m10"]/ M["m00"])
                centerY = int(M["m01"] / M["m00"])
                xs.append(centerX)
                ys.append(centerY)

        centroid = (int(sum(xs) / len(xs)), int(sum(ys) / len(ys))) if len(xs) != 0 else None
        radius = (totalArea / np.pi) ** 0.5

        cv2.drawContours(frame, contours, -1, (0, 255, 0), thickness=5)
        cv2.circle(frame, centroid, 5, (255, 0, 0), thickness=10)
        return Ball(centroid, radius, "color and contour")


class ObjectDetector(BallDetector):
    def detect(frame) -> Ball:
        classNames = []
        classPath = os.path.dirname(os.path.realpath(__file__)) + "/coco.names"
        with open(classPath, "r") as classFile:
            classNames = classFile.read().rstrip("\n").split("\n")
            configPath = (os.path.dirname(os.path.realpath(__file__)) + "/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
            weightsPath = (os.path.dirname(os.path.realpath(__file__)) + "/frozen_inference_graph.pb")

            net = cv2.dnn_DetectionModel(weightsPath, configPath)
            net.setInputSize(320, 320)
            net.setInputScale(1.0 / 127.5)
            net.setInputMean((127.5, 127.5, 127.5))
            net.setInputSwapRB(True)

        return Ball()