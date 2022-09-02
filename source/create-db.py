import cv2
import os
import numpy
import sys
from termcolor import cprint

from helpers.filehelpers import *
from helpers.facehelpers import *
from helpers.recognizerhelpers import *

from globalvars import *

rollNo = 0
studentName = ""

def main () :
	classifier = cv2.CascadeClassifier (classifierFile)
	camera = cv2.VideoCapture (camPort)

	moreToAdd = 'Y'

	while moreToAdd[0] == 'Y' or moreToAdd[0] == 'y':
		cprint ("Enter the Student's Name: ", "blue", end = "")
		studentName = input ()
		while True :
			try :
				cprint ("Enter the Student's Roll Number (-1 to cancel this entry): ", "blue", end = "")
				rollNo = int (input ())
				break
			except ValueError :
				cprint ("Invalid value for roll no!", "red", attrs = ["bold"])
		if (recordExists (rollNo, recordFilePath)) :
			cprint (f"Roll No. {rollNo} already exists, overWrite (y/N) ? ", "yellow", end = "")
			choiceToEraseRecord = input ().upper ()
			if (choiceToEraseRecord == "Y") :
				eraseRecord (rollNo, recordFilePath)
			else :
				continue

		# provide a way to undo the last entry
		elif (rollNo == -1):
			cprint ("Recieved -1 as roll no, skipping entry", "magenta")
			cprint ("Do you want to add more Students? (y/N): ", "blue", end = "")
			moreToAdd = input ()
			continue

		# keep showing detected faces
		while True :
			_, frame = camera.read ()
			# resize image for easier processing
			frame = cv2.resize (frame, (int (frame.shape[1] * imageProcessingScale), int (frame.shape[0] * imageProcessingScale)))
			# processing done in grayscale
			grayFrame = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
	
			detectedFacesCoordinates = classifier.detectMultiScale (grayFrame, faceDetectionScale, neighbouringPixels)
	
			for (x, y, w, h) in detectedFacesCoordinates :
				cv2.rectangle (frame, (x, y), (x + w, y + w), 100, 4)
	
			cv2.imshow ("Video Feed", frame)
			key = cv2.waitKey (1)
	
			# user pressed space, hence, click photo
			if (key == ord (" ")) :
				break

		cv2.destroyAllWindows ()
		
		
		addRecord (rollNo, studentName, recordFilePath)
		capturedFaces = captureFacesFromCamera (camera, imageProcessingScale, classifier, faceDetectionScale, neighbouringPixels, 20)
		writeFaces (capturedFaces, rollNo, dataPath)
		
		cprint ("Do you want to add more Students? (y/N): ", "blue", end = "")
		moreToAdd = input ()

main ()

# save the newly created recognizer
faceRecognizer = cv2.face.LBPHFaceRecognizer.create ()
updateRecognizer (faceRecognizer, faceRecognizerFilePath, dataPath)

