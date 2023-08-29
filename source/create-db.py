import cv2
import os
from termcolor import cprint

from helpers.filehelpers import *
from helpers.facehelpers import *
from helpers.recognizerhelpers import *

from globalvars import *

rollNo = 0
studentName = ""

if (not os.path.exists (recordFilePath)) :
	file = open (recordFilePath, "a")
	file.close ()

if (not os.path.exists (dataPath)) :
	os.mkdir (dataPath)

def main () :
	classifier = cv2.CascadeClassifier (classifierFile)
	camera = cv2.VideoCapture (camPort)

	moreToAdd = 'Y'

	while moreToAdd[0] == 'Y' or moreToAdd[0] == 'y':
		cprint ("Enter the Student's Name (or 'REM' to remove a previous entry)", "blue", attrs = ["bold"], end = "")
		studentName = input ()
		while True :
			try :
				cprint ("Enter the Student's Roll Number (-1 to cancel this entry): ", "blue", attrs = ["bold"], end = "")
				rollNo = int (input ())
				break
			except ValueError :
				cprint ("Invalid value for roll no!", "red", attrs = ["bold"])

		# provide a way to undo the last entry
		if (rollNo == -1):
			cprint ("Recieved -1 as roll no, skipping entry", "magenta", attrs = ["bold"])
			cprint ("Do you want to add more Students? (y/N): ", "blue", attrs = ["bold"], end = "")
			moreToAdd = input ()
			continue

		# provide a way to remove records if the roll no entered was not -1
		elif (studentName == "REM") :
			if (not recordExists (rollNo, recordFilePath)) :
				cprint ("Record to delete does not exist!", "red", attrs = ["bold"])
				continue
			else :
				eraseRecord (rollNo, recordFilePath)
				cprint (f"Record of Roll No. `{rollNo}` erased", "green", attrs = ["bold"])
			cprint ("Do you want to add more Students? (y/N): ", "blue", attrs = ["bold"], end = "")
			moreToAdd = input ()
			continue

		if (recordExists (rollNo, recordFilePath)) :
			cprint (f"Roll No. {rollNo} already exists, overWrite (y/N) ? ", "yellow", attrs = ["bold"], end = "")
			choiceToEraseRecord = input ().upper ()
			if (choiceToEraseRecord == "Y") :
				eraseRecord (rollNo, recordFilePath)
			else :
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

		
		addRecord (rollNo, studentName, recordFilePath)
		capturedFaces = captureFacesFromCamera (camera, imageProcessingScale, classifier, faceDetectionScale, neighbouringPixels, 20)
		cv2.destroyAllWindows ()
		writeFaces (capturedFaces, rollNo, dataPath)
		
		cprint ("Do you want to add more Students? (y/N): ", "blue", attrs = ["bold"], end = "")
		# to handle empty inputs
		moreToAdd = input () + " "

main ()

# save the newly created recognizer
faceRecognizer = cv2.face.LBPHFaceRecognizer_create ()
updateRecognizer (faceRecognizer, faceRecognizerFilePath, dataPath)

