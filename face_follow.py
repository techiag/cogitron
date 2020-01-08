from io import BytesIO
#from picamera import PiCamera
import cv2
import numpy as np
import os

# set to true if captures are too slow
# the video port bypasses some postprocessing, sacrificing quality for framerate
USE_VIDEO_PORT = False
RESOLUTION = (1296, 972) # (width, height). use a 4:3 resolution for max FOV

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
        self.cap = cv2.VideoCapture(0)
        #self.cam = PiCamera(resolution=RESOLUTION)
        self.buf = np.empty(shape, dtype=np.uint8)

    def recoginze(self):
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascades.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        print(faces)
        return faces

    #def recognize_pi(self):
        #cam.capture(self.buf, format="bgr", use_video_port=USE_VIDEO_PORT)
        #frame = buf[:RESOLUTION[1],:RESOLUTION[0]] # slice off padding pixels
        #assert frame.base is buf # make sure slicing doesn't copy
        #value = self.convolution_nn.recoginze(frame)
        #print(value)
        #return value

sr = Sauron()
sr.recoginze()