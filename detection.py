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
            if area < 200:
            # if area < 750:
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

        cv2.drawContours(frame, largeContours, -1, (0, 255, 0), thickness=5)
        if centroid is not None:
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


class AngleDetection():
    def detect(frame):
        gray = cv2.bitwise_not(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        horizontal = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                cv2.THRESH_BINARY, 15, -2)
        cols = horizontal.shape[1]
        horizontal_size = cols // 30
        horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
        horizontal = cv2.morphologyEx(horizontal, cv2.MORPH_OPEN, horizontalStructure)
        blurred = cv2.GaussianBlur(horizontal, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 90, 15, None,
                            50, 10)

        degList = []
        if lines is not None:
            for line in lines:
                for x1,y1,x2,y2 in line:
                    deg = np.degrees(np.arctan((y2-y1)/(x2-x1)))
                    if abs(deg) < 10:
                        cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),5)
                        degList.append(deg)
        if len(degList) > 0:
            return sum(degList) / len(degList)
        return None
