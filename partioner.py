import os
import libGeneral

############################################
PARTITIONING_PATH = "u4_eval/"
############################################

dirs = os.listdir(PARTITIONING_PATH)
for subdir in dirs:
	files = os.listdir(PARTITIONING_PATH + subdir)
	nrOfFiles = len(files)
	nrOfTrainingFiles = nrOfFiles / 2
	nrOfTestingFiles = nrOfFiles - nrOfTrainingFiles

	# make directories
	trainingDir  = PARTITIONING_PATH + subdir + "/train"
	testingDir = PARTITIONING_PATH + subdir + "/test"
	os.mkdir(trainingDir)
	os.mkdir(testingDir)
	
	#move files
	counter = 0
	for f in files:
		if counter < nrOfTrainingFiles:
			os.rename(PARTITIONING_PATH + subdir + "/" + f, PARTITIONING_PATH + subdir + "/train/" + f)
		else:
			os.rename(PARTITIONING_PATH + subdir + "/" + f, PARTITIONING_PATH + subdir + "/test/" + f)
		counter += 1
	
	#test number of files
	nrOfMovedTrainingFiles = len(os.listdir(trainingDir))
	nrOfMovedTestingFiles = len(os.listdir(testingDir))
	
	if nrOfMovedTrainingFiles == nrOfTrainingFiles and nrOfMovedTestingFiles == nrOfTestingFiles:
		print subdir + ": OK"
	else:
		print subdir + ": ERROR"
	
