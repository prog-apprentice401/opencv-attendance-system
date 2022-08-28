import os
import numpy
import cv2

from helpers.facehelpers import *
from helpers.filehelpers import *

from globalvars import *

cascade_classifier = cv2.CascadeClassifier ('harrcascade_frontalface_default.xml')
