import os


imageProcessingScale = 0.75

faceDetectionScale = 1.2
neighbouringPixels = 10

camPort = 0

_assetsDirectory = "assets"

_recordFileName = "data_10A.rec"
_dataDirectory = "datasets"
_attendanceDirectory = "attendance"

classifierFile = os.path.join (_assetsDirectory, 'haarcascade_frontalface_default.xml')
recordFilePath = os.path.join (_assetsDirectory, _recordFileName)
dataPath = os.path.join (_assetsDirectory, _dataDirectory)
attendanceDirectoryPath = os.path.join (_assetsDirectory, _attendanceDirectory)

_faceRecognizerFileName = "faceRecognizer.bin"
faceRecognizerFilePath = os.path.join (_assetsDirectory, _faceRecognizerFileName)
