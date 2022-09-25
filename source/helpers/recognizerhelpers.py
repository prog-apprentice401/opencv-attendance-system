import cv2
import numpy
import os

from termcolor import cprint

def getFacesAndLabels (dataPath) :
	labels = []
	faces = []

	for studentFolder in os.listdir (dataPath) :
		# ignore invalid folders
		if (not studentFolder.startswith ('s')):
			continue
		try:
			currentLabel = int (studentFolder[1:])
		except ValueError :
			cprint (f"Folder `{studentFolder}` is named incorrectly, cannot process. Skipping", "magenta", attrs = ["bold"])
			continue

		studentFolderPath = os.path.join (dataPath, studentFolder)
		for imageName in os.listdir (studentFolderPath) :
			labels.append (currentLabel)
			# always read in grayscale
			faces.append (cv2.imread (os.path.join (studentFolderPath, imageName), cv2.IMREAD_GRAYSCALE))
	labels = numpy.array (labels)
	
	return faces, labels

def updateRecognizer (faceRecognizer, faceRecognizerFilePath, dataPath) :
	faces, labels = getFacesAndLabels (dataPath)
	cprint (f"{len (faces)} faces found with {len (labels)} label. Training...", "green", attrs = ["bold"])
	try :
		faceRecognizer.update (faces, labels)
	except :
		cprint ("Something real wrong happened with the face recognizer, training afresh", "magenta", attrs = ["bold"])
		faceRecognizer.train (faces, labels)
	cprint ("Done Training", "green", attrs = ["bold"])

	faceRecognizer.save (faceRecognizerFilePath)

	return faceRecognizer

def safeLoadRecognizer (faceRecognizer, faceRecognizerFilePath, dataPath) :
	try :
		faceRecognizer.read (faceRecognizerFilePath)
	except :
		cprint (f"Could not load face recognizer from file `{faceRecognizerFilePath}`, creating new", "magenta", attrs = ["bold"])
		updateRecognizer (faceRecognizer, faceRecognizerFilePath, dataPath)
	return faceRecognizer
