import cv2

class Basketball:

    def __init__(self, contours):
        self.contours = contours
        self._calculateCentroidAndArea()

    def _calculateCentroidAndArea(self):
        xs = []
        ys = []
        totalArea = 0

        for contour in self.contours:
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

        if len(xs) != 0:
            self.centroid = (int(sum(xs) / len(xs)), int(sum(ys) / len(ys)))

        self.area = totalArea

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)