import os

classifierFile = os.path.join ('assets', 'haarcascade_frontalface_default.xml')

imageProcessingScale = 0.75

faceDetectionScale = 1.2
neighbouringPixels = 10

camPort = 0

_assetsDirectory = "assets"

_recordFileName = "data_10A.rec"
_dataDirectory = "datasets"

recordFilePath = os.path.join (_assetsDirectory, _recordFileName)
dataPath = os.path.join (_assetsDirectory, _dataDirectory)

_faceRecognizerFileName = "faceRecognizer.bin"
faceRecognizerFilePath = os.path.join (_assetsDirectory, _faceRecognizerFileName)
