import os
import cv2
from datetime import date
from termcolor import cprint

from helpers.facehelpers import *
from helpers.filehelpers import *
from helpers.recognizerhelpers import *
from helpers.attendancehelpers import *

from globalvars import *

classifier = cv2.CascadeClassifier (classifierFile)
camera = cv2.VideoCapture (camPort)
faceRecognizer = cv2.face.LBPHFaceRecognizer_create ()
faceRecognizer = safeLoadRecognizer (faceRecognizer, faceRecognizerFilePath, dataPath)

today = date.today ()
attendanceFilePath = os.path.join (attendanceDirectoryPath, today.strftime ("%Y_%m_%d.record"))

if (not os.path.exists (attendanceDirectoryPath)) :
	print ("Did not find, attendance directory, creating new")
	os.mkdir (attendanceDirectoryPath)

while True :
	face = captureFacesFromCamera (camera, imageProcessingScale, classifier, faceDetectionScale, neighbouringPixels, 1)[0]
	label = faceRecognizer.predict (face)
	rollNo = label[0]
	cprint (f"Roll number found : {rollNo}", "yellow")
	markAttendance (rollNo, attendanceFilePath, recordFilePath, True)
