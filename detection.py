from abc import ABC, abstractmethod
import cv2

class Ball:
    def __init__(self, centroid, area, detection_method):
        self.centroid = centroid
        self.area = area
        self.detection_method = detection_method
    
    def __str__(self):
        return f"Basketball {{ centroid: {self.centroid}, area: {self.area} }} (detected with {self.detection_method}"

class BallDetector(ABC):
    @abstractmethod
    def detect(frame) -> Ball

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
        cv2.drawContours(frame, contours, -1, (0, 255, 0), thickness=5)

        xs = []
        ys = []
        totalArea = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 130:
                continue
            totalArea += area

            M = cv2.moments(contour)
            if M["m00"] != 0:
                centerX = int(M["m10"]/ M["m00"])
                centerY = int(M["m01"] / M["m00"])
                xs.append(centerX)
                ys.append(centerY)

        centroid = (int(sum(xs) / len(xs)), int(sum(ys) / len(ys))) if len(xs) != 0 else None
        area = totalArea

        return Ball(centroid, area, "color and contour")