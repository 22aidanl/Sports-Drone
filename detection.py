from abc import ABC, abstractmethod
# from tracker import findBestCircularity
import cv2
import os
import numpy as np
import math

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

    def __init__(self):
        self.lastPos = None

    def detect(self, frame) -> Ball:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        bballLower = np.array([10/360, 40/100, 20/100])
        bballUpper = np.array([30/360, 100/100, 100/100])
        
        # Convert to OpenCV ranges
        bballLower[0] *= 179
        bballUpper[0] *= 179
        bballLower[1:] *= 255
        bballUpper[1:] *= 255

        mask = cv2.inRange(hsv, bballLower, bballUpper)
        gray = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((15, 15)))
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
       

        contourFrame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(contourFrame, contours, -1, (0, 255, 0), thickness=2)
        cv2.imshow("Contours", contourFrame)

        contours = [contour for contour in contours if cv2.contourArea(contour) > 200]

        if len(contours) > 0:
            contourIndex = findBestCircularity(contours)
            if contourIndex is not None:
                ((x, y), radius) = cv2.minEnclosingCircle(contours[contourIndex])
                x, y = int(x), int(y)
                print(x, y, radius)
                if radius > 25:
                    
                    if self.lastPos is None:
                        self.lastPos = (x, y)
                    elif math.dist(self.lastPos, (x, y)) < 50:
                        self.lastPos = (x, y)
                        cv2.circle(frame, (x, y), int(radius),
                                    (0, 255, 255), 2)
                        return Ball((x, y), radius, "color and contour")

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


def findBestCircularity(contours):
    bestCircularity = 0
    bestContour = None

    #DEBUG
    circularityList = []

    for i, contour in enumerate(contours):
        perimeter = cv2.arcLength(contour, True)
        area = cv2.contourArea(contour)
        if perimeter == 0:
            continue
        circularity = (4 * math.pi * area) / (perimeter ** 2)

        #DEBUG
        circularityList.append(circularity)
        if circularity > bestCircularity:
            bestCircularity = circularity
            bestContour = i

    #DEBUG
    # if bestContour is None:
    return bestContour


class AngleDetector():
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