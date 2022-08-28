import numpy
import cv2
import os

def extractFacesFromImage (image, classifier, scale, neighbours) :
	grayImage = cv2.cvtColor (image, cv2.COLOR_BGR2GRAY)
	facesCoordinates = classifier.detectMultiScale (image, scale, neighbours)
	faces = []

	for (x, y, w, h) in facesCoordinates :
		faces.append (image[y:y + h, x:x + h])
	
	return faces

def captureFacesFromCamera (camera, processingScale, classifier, faceDetectionScale, neighbouringPixels) :
	capturedFaces = []
	faceList = []

	for i in range (5) :
		while True :
			(_, frame) = camera.read ()
			frame = cv2.resize (frame, (int (frame.shape[1] * processingScale), int (frame.shape[0] * processingScale)))

			#use only the first face, and ignore the coordinates returned
			facesList = extractFacesFromImage (frame, classifier, faceDetectionScale, neighbouringPixels)
			if (len (facesList) > 0) :
				break
		face = facesList[0]
		capturedFaces.append (face)
		cv2.waitKey (20)
	
	return capturedFaces

def writeFaces (capturedFaces, rollNo, dataDirectory) :
	dataPath = os.path.join (dataDirectory, "s" + str (rollNo))

	if (not os.path.isdir (dataPath)) :
		os.mkdir (dataPath)
	else :
		choiceToOverwrite = input ("directory for requested roll no already exists, overwrite (y/N) ?")
		if (choiceToOverwrite != "y" and choiceToOverwrite != "Y") :
			print ("Skipping overwrite")
			return 

		for file in os.listdir (dataPath) :
			os.remove (os.path.join (dataPath, file))

	i = 0

	for face in capturedFaces :
		imagePath = os.path.join (dataPath, str (i) + ".png")
		cv2.imwrite (imagePath, face)
		i += 1
