import os
import numpy
import cv2
from datetime import date

from helpers.facehelpers import *
from helpers.filehelpers import *
from helpers.recognizerhelpers import *

from globalvars import *

classifier = cv2.CascadeClassifier (classifierFile)
camera = cv2.VideoCapture (camPort)
faceRecognizer = cv2.face.LBPHFaceRecognizer.create ()
faceRecognizer = safeLoadRecognizer (faceRecognizer, faceRecognizerFilePath, dataPath)

today = date.today ()
print (today.year, today.month, today.day)

while True :
	faces = captureFacesFromCamera (camera, imageProcessingScale, classifier, faceDetectionScale, neighbouringPixels)
	for face in faces :
		label = faceRecognizer.predict (face)
		print (label)
		#if (getRecordOf (label, recordFilePath)) :
		#	markPresent ()
