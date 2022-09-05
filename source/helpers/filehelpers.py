import numpy
import os
from termcolor import cprint

def splitRecord (line) :
	line = line.strip ()
	rollNumberLength = 0

	while (rollNumberLength < len (line) and line[rollNumberLength] != " ") :
		rollNumberLength += 1
	
	line = [line[0:rollNumberLength], line[rollNumberLength:]]
	for i in range (len (line)) :
		line[i] = line[i].strip ()

	return line

def getRecordOf (rollNo, recordFilePath) :
	# compare as string, so that if a single record in file is corrupted
	# error is not raised while turning THAT to int
	line = None
	recordFile = None

	try :
		recordFile = open (recordFilePath, "r")
	except FileNotFoundError :
		cprint (f"Error Opening File: `{recordFilePath}`", "red", attrs = ["bold"])
		return None

	try :
		while (line := recordFile.readline ()) :
			# skip empty lines
			if (len (line) < 2) :
				continue
			line = splitRecord (line)
			if (rollNo == int (line[0])) :
				return line
		# not found
		return None
	except ValueError :
		cprint (f"Error processing information, record file `recordFilePath` seems to be corrupted", "red", attrs = ["bold"])
		return None
	finally :
		recordFile.close ()
	

def recordExists (rollNo, recordFilePath) :
	if (getRecordOf (rollNo, recordFilePath)) :
		return True
	else :
		return False

def eraseRecord (rollNo, recordFilePath) :
	recordFile = None
	tempRecordFile = None

	try :
		recordFile = open (recordFilePath, "r")
		tempRecordFile = open (recordFilePath + ".tmp", "w")
	except FileNotFoundError :
		cprint (f"Error opening required files: `{recordFilePath}, `{recordFilePath}.tmp`", "red", attrs = ["bold"])
		return -1

	try :
		while (line := recordFile.readline ()) :
			line = splitRecord (line)
			# skip  record to delete
			if (int (line[0]) == rollNo) :
				continue
			# write all other records
			tempRecordFile.write (line[0] + line[1] + '\n')
	except ValueError :
		cprint (f"Error processing roll numbers. `{recordFilePath}` seems to be corrupted", "red", attrs = ["bold"])
	finally :
		recordFile.close ()
	os.remove (recordFilePath)
	# make the updated file the new default
	os.rename (recordFilePath + ".tmp", recordFilePath)


def addRecord (rollNo, studentName, recordFilePath) :
	recordFile = None
	tempRecordFile = None
	recordAdded = False
	
	try :
		recordFile = open (recordFilePath, "r")
		tempRecordFile = open (recordFilePath + ".tmp", "w")
	except FileNotFoundError :
		cprint (f"Error opening required files: `{recordFilePath}, `{recordFilePath}.tmp`", "red", attrs = ["bold"])
		return -1

	try :
		while (line := recordFile.readline ()) :
			line = splitRecord (line)
			if (int (line[0]) > rollNo and not recordAdded) :
				tempRecordFile.write (str (rollNo) + " " + studentName + "\n")
				recordAdded = True
			tempRecordFile.write (line[0] + " " + line [1] + "\n")

		if (not recordAdded) :
			tempRecordFile.write (str (rollNo) + " " + studentName + "\n")
			recordAdded = True
	except ValueError :
		cprint (f"Error processing roll numbers. `{recordFilePath}` seems to be corrupted", "red", attrs = ["bold"])
	finally :
		recordFile.close ()
		tempRecordFile.close ()

	os.remove (recordFilePath)
	# make the updated file the new default
	os.rename (recordFilePath + ".tmp", recordFilePath)
