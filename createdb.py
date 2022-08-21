import os
import cv2

cam_port = 0
webcam = cv2.VideoCapture (cam_port)

classifierFile = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier (classifierFile)

finalWidth = 150
finalHeight = 200

dataPath = 'datasets'
student = ''	#name for current student

currentFacesCoordinates = [] 	#list to hold current face coordinates

def emptyDirectory (path) :
	for root, directories, files in os.walk (path) :
		for f in files :
			os.remove (os.path.join (root, f))

while True :
	student = input ("Enter name of current Student: ")

	#ensure data folder exists
	path = os.path.join (dataPath, student)
	if (not os.path.isdir (path)) :
		os.mkdir (path)
	else :
		choice = input ("Records already exist. Overwrite? (y/N)")
		if (choice != 'y' and choice != 'Y') :
			continue
		else :
			emptyDirectory (path)

	# show rectangle around face as a marker
	while (True) :
		(_, im) = webcam.read ()
		im = cv2.resize (im, (int (im.shape[1] * 0.5), int (im.shape[0] * 0.5)))
		gray = cv2.cvtColor (im, cv2.COLOR_BGR2GRAY)

		currentFacesCoordinates = face_cascade.detectMultiScale (gray, 1.3, 4)

		for (x, y, w, h) in currentFacesCoordinates:
			cv2.rectangle (im, (x, y), (x + w, y + h), 20)
		cv2.imshow ('face', im)
		k = cv2.waitKey (1)
		if (k == ord (' ')) :
			break

	for i in range (5): 
		(_, im) = webcam.read ()
		im = cv2.resize (im, (int (im.shape[1] * 0.5), int (im.shape[0] * 0.5)))
		gray = cv2.cvtColor (im, cv2.COLOR_BGR2GRAY)

		currentFacesCoordinates = face_cascade.detectMultiScale (gray, 1.3, 4)

		cv2.imshow ('face', im)
		k = cv2.waitKey (2)
		
		face = gray[y : y + h, x : x + w]
		cv2.imwrite (os.path.join (path, str(i) + '.png'), face)
	cv2.destroyAllWindows ()

