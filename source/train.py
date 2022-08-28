import os
import numpy
import cv2

cascade_classifier = cv2.CascadeClassifier ('haarcascade_frontalface_default.xml')

webcam = cv2.VideoCapture (0)
imageScale = 0.75
face_recognizer = cv2.face.LBPHFaceRecognizer.create ()

trainingFaces = []
for file in os.listdir ('datasets/Himanshu') :
	face = cv2.imread ('datasets/Himanshu/' + file, cv2.IMREAD_GRAYSCALE)
	trainingFaces.append (face)

for file in os.listdir ('datasets/Koustubh Srivastava') :
	face = cv2.imread ('datasets/Koustubh Srivastava/' + file, cv2.IMREAD_GRAYSCALE)
	trainingFaces.append (face)

face_recognizer.train (trainingFaces, numpy.array ([1, 1, 1, 1, 1, 2, 2, 2, 2, 2]))
print ("trained")

while True:
	detectedFaces = []
	while True:
		_, frame = webcam.read ()
		frame = cv2.resize (frame, (int (frame.shape[1] * imageScale), int (frame.shape[0] * imageScale)))
		grayFrame = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
	
		detectedFaces = cascade_classifier.detectMultiScale (grayFrame, 1.3, 2)
		if (len (detectedFaces) > 0) :
			break
	
	x, y, w, h = detectedFaces[0]
	if (w > 50 and h > 50) :
		continue

	print (x, y, w, h)
	cv2.rectangle (frame, (x, y), (x + w, y + h), 100, 4)
	cv2.imshow ('video', frame)
	face = grayFrame[x : x + w, y : y + h]
	
	try:
		label = face_recognizer.predict (face)
	except:
		cv2.imshow (face)
		cv2.waitKey (0)
		exit (-1)
	print (type (label))
