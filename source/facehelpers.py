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

def captureFacesFromVideo (camera, processingScale, classifier, faceDetectionScale, neighbouringPixels) :
	capturedFaces = []
	for i in range (5) :
		(_, frame) = camera.read ()
		frame = cv2.resize (frame, (int (frame.shape[1] * processingScale), int (frame.shape[0] * processingScale)))

		#use only the first face, and ignore the coordinates returned
		facesList = extractFacesFromImage (frame, classifier, faceDetectionScale, neighbouringPixels)
		face = facesList[0]
		capturedFaces.append (face)
		cv2.waitKey (20)
	
	return capturedFaces

def writeFaces (capturedFaces, rollNo, dataDirectory) :
	dataPath = os.path.join (dataDirectory, 's' + str (rollNo))

	if (not os.path.isdir (dataPath)) :
		os.mkdir (dataPath)
	else :
		choiceToOverwrite = input ('directory for requested roll no already exists, overwrite (y/N) ?')
		if (choiceToOverwrite == 'y' or choiceToOverwrite == 'Y') :
			return 

		for file in os.listdir (dataPath) :
			remove (os.path.join (dataPath, file))

	i = 0

	for face in capturedFaces :
		imagePath = os.path.join (dataPath, str (i) + '.png')
		cv2.imwrite (imagePath, face)
		i += 1
