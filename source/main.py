import os
import numpy
import cv2

from helpers.facehelpers import *
from helpers.filehelpers import *
from helpers.recognizerhelpers import *

from globalvars import *

classifier = cv2.CascadeClassifier (classifierFile)
camera = cv2.VideoCapture (camPort)
faceRecognizer = cv2.face.LBPHFaceRecognizer ()
faceRecognizer = safeLoadRecognizer (faceRecognizer, faceRecognizerFilePath, dataPath)

