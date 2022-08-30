import cv2
import os
import numpy
import sys

from helpers.filehelpers import *
from helpers.facehelpers import *
from helpers.recognizer import *

from globalvars import *

rollNo = 0
studentName = ""

def main () :
	classifier = cv2.CascadeClassifier (classifierFile)
	camera = cv2.VideoCapture (camPort)

	moreToAdd = 'Y'

	while moreToAdd[0] == 'Y' or moreToAdd[0] == 'y':
		studentName = input ("Enter the Student's Name: ")
		rollNo = int (input ("Enter the Student's Roll Number (-1 to cancel this entry) :"))

		if (recordExists (rollNo, recordFilePath)) :
			choiceToEraseRecord = input (f"Roll No. {rollNo} already exists, overWrite (y/N) ? ").upper ()
			if (choiceToEraseRecord == "Y") :
				eraseRecord (rollNo, recordFilePath)
			else :
				continue

		# provide a way to undo the last entry
		elif (rollNo == -1):
			print ("Recieved -1 as roll no, skipping entry")
			moreToAdd = input ("Do you want to add more Students? (y/N): ")
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
	
			# user pressed space or enter, hence, click photo
			if (key == ord (" ") or key == ord ("\n")) :
				break

		cv2.destroyAllWindows ()
		
		addRecord (rollNo, studentName, recordFilePath)
		capturedFaces = captureFacesFromCamera (camera, imageProcessingScale, classifier, faceDetectionScale, neighbouringPixels)
		writeFaces (capturedFaces, rollNo, dataPath)
		
		
		moreToAdd = input ("Do you want to add more Students? (y/N): ")

main ()

# save the newly created recognizer
faceRecognizer = cv2.face.LBPHFaceRecognizer ()
faceRecognizer = updateRecognizer (faceRecognizer, faceRecognizerFilePath, dataPath)

