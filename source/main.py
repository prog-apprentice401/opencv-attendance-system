import cv2
import os
import numpy

# helper functions defined in the same directory
from filehelpers import *
from facehelpers import *

# custom file
#import trainer

faceDetectionScale = 1.2
neighbouringPixels = 10

cam_port = 0

processingScale = 0.75
classifierFile = os.path.join ("opencv-files", "haarcascade_frontalface_default.xml")

rollNo = 0
studentName = ""
recordFileName = "data_10A.rec"
dataDirectory = "datasets"

recordFilePath = os.path.join (os.getcwd (), recordFileName)
dataPath = os.path.join (os.getcwd (), dataDirectory)

def main () :
	classifier = cv2.CascadeClassifier (classifierFile)
	camera = cv2.VideoCapture (cam_port)

	moreToAdd = True
	while True:
		studentName = input ("Enter the Student's Name: ")
		rollNo = int (input ("Enter the Student's Roll Number: "))

		if (recordExists (rollNo, recordFilePath)) :
			choiceToEraseRecord = input (f"Roll No. {rollNo} already exists, overWrite (y/N) ? ").upper ()
			if (choiceToEraseRecord == "Y") :
				eraseRecord (rollNo, recordFilePath)
			else :
				continue

		# keep showing detected faces
		while True :
			_, frame = camera.read ()
			# resize image for easier processing
			frame = cv2.resize (frame, (int (frame.shape[1] * processingScale), int (frame.shape[0] * processingScale)))
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
		capturedFaces = captureFacesFromCamera (camera, processingScale, classifier, faceDetectionScale, neighbouringPixels)
		writeFaces (capturedFaces, rollNo, dataPath)
		
		moreToAdd = input ("Do you want to add more Students? (y/N): ")

		# indexes to ensure functioning even if the entire word is typed
		if (moreToAdd != "y" and moreToAdd != "Y") :
			break

main ()
