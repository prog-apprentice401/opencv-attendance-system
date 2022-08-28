import cv2
import numpy
import os
import pickle

def loadRecognizer (faceRecognizerFilePath) :
	faceRecognizer = None
	faceRecognizerFile = None

	if (os.path.exists (faceRecognizerFilePath)) :
		try :
			faceRecognizerFile = open (faceRecognizerFilePath, "rb")
		except :
			print (f"Error! Could not open file {faceRecognizerFilePath}.\n"
			       "Failed to load faceRecognizer")
			return None
	else :
		print (f"Recognizer file `{faceRecognizerFilePath}` does not exist, create new")
		return None
	
	try :
		faceRecognizer = pickle.load (faceRecognizerFile)
	except :
		print ("Error loading faceRecognizer")
		return None

	return faceRecognizer

def saveRecognizer (faceRecognizer, faceRecognizerFilePath) :
	faceRecognizerFile = None

	try :
		faceRecognizerFile = open (faceRecognizerFilePath, "wb")
	except :
		print (f"Error! Could not open file `{faceRecognizerFilePath}` for writing")
		return -1

	try :
		pickle.dump (faceRecognizer, faceRecognizerFile)
	except :
		print (f"Error writing to file `{faceRecognizerFilePath}`")
		return None
	finally :
		faceRecognizerFile.close ()

def getFacesAndLabels (dataPath) :
	labels = []
	faces = []

	for studentFolder in os.listdir (dataPath) :
		# ignore invalid folders
		if (not studentFolder.startsWith ('s')):
			continue
		try:
			currentLabel = int (studentFolder[1:0])
		except ValueError :
			print (f"Folder `{studentFolder}` is named incorrectly, cannot process. Skipping")
			continue

		studentFolderPath = os.join (datapath, studentFolder)
		for imageName in os.listdir (studentFolderPath) :
			labels.append (currentLabel)
			faces.append (cv2.imread (os.path.join (studentFolderPath, imagename)))
	
	return faces, labels

def trainRecognizer (dataPath) :
	studentFaceDataPath = os.join (dataPath, "s" + rollNo)

	if (not os.path.exists (studentFaceDataPath)) :
		print ("The requested student's data does not exist")
		return None

	faceRecognizer = cv2.face.LBPHFaceRecognizer.create ()
	
	faces, labels = getFaceAndLabels (dataPath)

	faceRecognizer.train (faces, labels)

	return faceRecognizer

def updateRecognizer (datapath, faceRecognizerFilePath) :
	faceRecognizer = trainRecognizer (dataPath)
	saveRecognizer (faceRecognizer, faceRecognizerFilePath)
	return faceRecognizer
