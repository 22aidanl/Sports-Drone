import socket
import h264decoder
import numpy as np
import threading
import cv2
from time import sleep

address = ("192.168.10.1", 8889)
commandSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
videoSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

commandSocket.bind(("", 8889))
videoSocket.bind(("", 11111))
commandSocket.sendto(b"command", address)
commandSocket.sendto(b'streamon', address)

decoder = h264decoder.H264Decoder()

currentFrame = None


def receiveVideo():
    packet = b""
    while True:
        received, _ = videoSocket.recvfrom(2048)
        packet += received

        if len(received) != 1460:
            for frame in decodeH264(packet):
                global currentFrame
                currentFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            packet = b""

def decodeH264(packet):
    frameList = []
    frames = decoder.decode(packet)
    for frame in frames:
        (frame, w, h, ls) = frame
        if frame is not None:
            frame = np.frombuffer(frame, dtype=np.ubyte, count=len(frame))
            frame = frame.reshape((h, ls // 3, 3))
            frame = frame[:, :w, :]
            frameList.append(frame)
    return frameList

receiveVideoThread = threading.Thread(target=receiveVideo)
receiveVideoThread.daemon = True
receiveVideoThread.start()

while True:
    if currentFrame is not None:
        cv2.imshow("Tello Camera", currentFrame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
