import cv2
import os
import numpy as np
from djitellopy import tello


my_drone = tello.Tello()
my_drone.connect()
my_drone.streamon()
print(my_drone.get_battery())

while True:
    classNames = []
    classPath = os.path.dirname(os.path.realpath(__file__)) + "/coco.names"
    with open(classPath, "r") as classFile:
        classNames = classFile.read().rstrip("\n").split("\n")
        name_color = np.random.uniform(0, 255, size=(len(classNames), 3))
        configPath = (os.path.dirname(os.path.realpath(__file__)) + "/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
        weightsPath = (os.path.dirname(os.path.realpath(__file__)) + "/frozen_inference_graph.pb")

        net = cv2.dnn_DetectionModel(weightsPath, configPath)
        net.setInputSize(320, 320)
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)

        while True:
            frame = my_drone.get_frame_read().frame
            classIds, confs, bbox = net.detect(frame, confThreshold=0.18)

            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):

                if classId == 37:
                    cv2.rectangle(frame, box, color=(0,255,0), thickness=2)
                    cv2.putText(frame, classNames[classId-1].upper(), (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                    cv2.putText(frame, str(round(confidence*100,2)), (box[0]+200, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

            cv2.imshow("Ball Detection", frame)
            cv2.waitKey(1)