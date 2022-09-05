import cv2
import os
from termcolor import cprint

def extractFacesFromImage (image, classifier, scale, neighbours) :
	facesCoordinates = classifier.detectMultiScale (image, scale, neighbours)
	faces = []

	for (x, y, w, h) in facesCoordinates :
		faces.append (image[y:y + h, x:x + h])
	
	return faces

def captureFacesFromCamera (camera, processingScale, classifier, faceDetectionScale, neighbouringPixels, numberOfImages) :
	capturedFaces = []

	for i in range (numberOfImages) :
		while True :
			(_, frame) = camera.read ()
			frame = cv2.resize (frame, (int (frame.shape[1] * processingScale), int (frame.shape[0] * processingScale)))
			grayFrame = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)

			#use only the first face, and ignore the coordinates returned
			facesList = extractFacesFromImage (grayFrame, classifier, faceDetectionScale, neighbouringPixels)
			if (len (facesList) > 0) :
				break
		capturedFaces.append (facesList[0])
		cv2.waitKey (20)
	
	return capturedFaces

def writeFaces (capturedFaces, rollNo, dataPath) :
	studentDataPath = os.path.join (dataPath, "s" + str (rollNo))

	if (not os.path.isdir (studentDataPath)) :
		os.mkdir (studentDataPath)
	else :
		cprint ("directory for requested roll no already exists, overwrite (y/N) ?", "yellow", attrs = ["bold"], end = "")
		choiceToOverwrite = input ()
		if (choiceToOverwrite != "y" and choiceToOverwrite != "Y") :
			cprint ("Skipping overwrite", "magenta", attrs = ["bold"])
			return 

		for file in os.listdir (studentDataPath) :
			os.remove (os.path.join (studentDataPath, file))

	i = 0

	for face in capturedFaces :
		imagePath = os.path.join (studentDataPath, str (i) + ".png")
		cv2.imwrite (imagePath, face)
		i += 1
