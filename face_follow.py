from io import BytesIO
from picamera import PiCamera
from cogitron import Cogitron
import cv2
import numpy as np
import os
import time
import math

# set to true if captures are too slow
# the video port bypasses some postprocessing, sacrificing quality for framerate
USE_VIDEO_PORT = False
#RESOLUTION = (1296, 972) # (width, height). use a 4:3 resolution for max FOV
RESOLUTION = (640, 480)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
face_cascades = cv2.CascadeClassifier(os.path.join(PROJECT_ROOT, "cascades/data/haarcascade_frontalface_alt2.xml"))

class Sauron:
    def __init__(self, convolution_nn=None):

        def ceil_mul(x, mul):
            mod = x % mul
            return x if mod == 0 else x + mul - mod

        shape = (ceil_mul(RESOLUTION[1], 16), ceil_mul(RESOLUTION[0], 32), 3)

        self.convolution_nn = convolution_nn
        #self.cam = PiCamera()
        #self.cap = cv2.VideoCapture(0)
        self.cam = PiCamera(resolution=RESOLUTION)
        self.cam.rotation = 180
        self.buf = np.empty(shape, dtype=np.uint8)

    def recoginze(self):
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascades.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        print(faces)
        return faces

    def recognize_pi(self):
        self.cam.capture(self.buf, format="bgr", use_video_port=USE_VIDEO_PORT)
        frame = self.buf[:RESOLUTION[1],:RESOLUTION[0]] # slice off padding pixels
        assert frame.base is self.buf # make sure slicing doesn't copy
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        value = face_cascades.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        print(value)
        return value

sr = Sauron()
center = (RESOLUTION[0] / 2, RESOLUTION[1] / 2)
yes = 45
no = 90
STEP = 5
cogitron = Cogitron()
resetcount = 10
while True:
    time.sleep(0.1)
    faces = sr.recognize_pi()
    if len(faces) == 0:
        resetcount -= 1
        if resetcount <= 0:
            yes = 45
            no = 90
    else:
        resetcount = 10
    nearest = (0, 0)
    nearest_dist = 1000000
    for face in faces:
        pos = (face[0] + face[2] / 2 - center[0], face[1] + face[3] / 2 - center[1])
        dist = pos[0] ** 2 + pos[1] ** 2
        if dist < nearest_dist:
            nearest = pos
            nearest_dist = dist
    print(nearest)
    if nearest[0] < 0:
        no = min(no + 5, 135)
    elif nearest[0] > 0:
        no = max(no - 5, 45)
    if nearest[1] > 0:
        yes = min(yes + 5, 70)
    elif nearest[1] < 0:
        yes = max(yes - 5, 40)
    cogitron.com.sendMessage(cogitron.com.motor_serial, "moveServo;0;" + str(no))
    time.sleep(0.1)
    cogitron.com.sendMessage(cogitron.com.motor_serial, "moveServo;1;" + str(yes))

