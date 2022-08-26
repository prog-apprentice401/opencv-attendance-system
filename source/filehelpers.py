import numpy
import os

def getRecordOf (rollNo, recordFilePath) :
	# compare as string, so that if a single record in file is corrupted
	# error is not raised while turning THAT to int
	line = None
	rollNo = str (rollNo)
	try:
		recordFile = open (recordFilePath, 'r')
		while (line := recordFile.readline ()) :
			line = line.split ()

			if (rollNo == line[0]) :
				break
		# not found
		line = None

	except:
		print (f"Error Opening File: `{recordFilePath}`")
	finally:
		recordFile.close ()
	
	return line


def recordExists (rollNo, recordFilePath) :
	if (getRecordOf (rollNo, recordFilePath)) :
		return True
	else :
		return False

# dummy function, not implemented yet
def eraseRecord (rollNo, recordFilePath) :
	0

# dummy function, not implemented yet
def addRecord (rollNo, studentName, recordFilePath) :
	0
