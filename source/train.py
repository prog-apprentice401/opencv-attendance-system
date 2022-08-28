import os
import numpy
import cv2

from helpers.facehelpers import *
from helpers.filehelpers import *
from helpers.recognizerhelpers import *

from globalvars import *

classifier = cv2.CascadeClassifier (classifierFile)
camera = cv2.VideoCapture (camPort)
faceRecognizer = None

# load saved recogniser
if (os.path.exists (faceRecognizerFilePath)) :
	try :
		faceRecognizer = loadRecognizer (faceRecognizerFilePath)
	except :
		faceRecognizer = updateRecognizer (dataPath, faceRecognizerFilePath)
# or make new one
else :
	faceRecognizer = updateRecognizer (dataPath, faceRecognizerFilePath)
