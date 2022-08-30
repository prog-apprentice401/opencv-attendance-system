import cv2
import numpy
import os

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
			print (f"Folder `{studentFolder}` is named incorrectly, cannot process. Skipping")
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
	print (f"{len (faces)} faces found with {len (labels)} label. Training...")
	try :
		faceRecognizer.update (faces, labels)
	except :
		print ("Something real wrong happened with the face recognizer, training afresh")
		faceRecognizer.train (faces, labels)
	print ("Done Training")

	faceRecognizer.save (faceRecognizerFilePath)

	return faceRecognizer

def safeLoadRecognizer (faceRecognizer, faceRecognizerFilePath, dataPath) :
	try :
		faceRecognizer.load (faceRecognizerFilePath)
	except :
		print (f"Could not load face recognizer from file `{faceRecognizerFilePath}`, creating new")
		updateRecognizer (faceRecognizer, faceRecognizerFilePath, dataPath)
	return faceRecognizer
