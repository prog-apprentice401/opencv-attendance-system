from helpers.filehelpers import *

def createAttendanceFile (attendanceFilePath, recordFilePath) :
	attendanceFile = None
	recordFile = None

	if (os.path.exists (attendanceFilePath)) :
		return -1
	try :
		attendanceFile = open (attendanceFilePath, "w")
	except :
		print (f"Cannot create file `{attendanceFilePath}`")
		return -1

	try :
		recordFile = open (recordFilePath, "r")
		while (line := recordFile.readline ()) :
			line = splitRecord (line)
			# start with unmarked attendance
			attendanceFile.write (str (line[0]) + " " + str (line[1]) + " " + "--\n")
	except :
		print (f"Cannot open file `{recordFilePath}`")
		return -1
	finally :
		attendanceFile.close ()
	

def splitAttendanceRecord (line) :
	line = line.strip ()
	rollNumberLength = 0
	# start with 1 to aid in negative indexing
	attendanceStatusLength = 1

	while (rollNumberLength < len (line) and line[rollNumberLength] != " ") :
		rollNumberLength += 1
	while (attendanceStatusLength <= len (line) and line[-attendanceStatusLength] != " ") :
		attendanceStatusLength += 1
	
	line = [line[0:rollNumberLength], line[rollNumberLength:-attendanceStatusLength], line [-attendanceStatusLength:]]
	for i in range (len (line)) :
		line[i] = line[i].strip ()

	return line

def markAttendance (rollNo, attendanceFilePath, recordFilePath, attendanceStatus) : 
	attendanceStatusStr = "PR" if attendanceStatus == True else "AB"

	if (not os.path.exists (attendanceFilePath)) :
		print (f"Could not find attendance file `{attendanceFilePath}`, creating new")
		createAttendanceFile (attendanceFilePath, recordFilePath)
	
	attendanceFile = None
	tempAttendanceFile = None

	try :
		attendanceFile = open (attendanceFilePath, "r")
		tempAttendanceFile = open (attendanceFilePath + ".tmp", "w")
	except FileNotFoundError :
		print (f"Error opening required files: `{attendanceFilePath}, `{attendanceFilePath}.tmp`")
		return -1

	try :
		while (line := attendanceFile.readline ()) :
			line = splitAttendanceRecord (line)

			# required record found
			if (int (line[0]) == rollNo) :
				print ("record for attendance marking found")
				line[2] = attendanceStatusStr
			tempAttendanceFile.write (line[0] + " " + line [1] + " " + line[2] + "\n")

	except :
		print (f"Error processing roll numbers. `{attendanceFilePath}` seems to be corrupted")
	finally :
		attendanceFile.close ()
		tempAttendanceFile.close ()

	os.remove (attendanceFilePath)
	# make the updated file the new default
	os.rename (attendanceFilePath + ".tmp", attendanceFilePath)
