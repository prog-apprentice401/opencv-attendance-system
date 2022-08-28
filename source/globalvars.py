import os

classifierFile = os.path.join ('opencv-files', 'haarcascade_frontalface_default.xml')

imageProcessingScale = 0.75

faceDetectionScale = 1.2
neighbouringPixels = 10

camPort = 0

recordFileName = "data_10A.rec"
dataDirectory = "datasets"

recordFilePath = os.path.join (os.getcwd (), recordFileName)
dataPath = os.path.join (os.getcwd (), dataDirectory)
