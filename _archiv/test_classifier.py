import libGeneral
import os
import bayes_classifier
import kNN_classifier

######################
GLOBAL_INDEX = "globalIndex";
EVAL_PATH = "u4_eval/"
######################

'''
OUTPUT: {class -> list(filename)}
'''
def divide():
	trainDict = {}
	testDict = {}
	
	dirs = os.listdir(EVAL_PATH)
	for subdir in dirs:
		files = os.listdir(EVAL_PATH + subdir)
		nrOfFiles = len(files)
		nrOfTrainingFiles = nrOfFiles / 2
		nrOfTestingFiles = nrOfFiles - nrOfTrainingFiles
		
		#divide files
		counter = 0
		listTrain = []
		listTest = []
		for f in files:	
			if counter < nrOfTrainingFiles:
				listTrain.append(f)
			else:
				listTest.append(f)
			counter += 1
			
		trainDict[subdir] = listTrain
		testDict[subdir] = listTest
		
		#test number of files
		nrOfDividedTrainingFiles = len(trainDict[subdir])
		nrOfDividedTestingFiles = len(testDict[subdir])
		
		if nrOfDividedTrainingFiles == nrOfTrainingFiles and nrOfDividedTestingFiles == nrOfTestingFiles:
			print subdir + ": OK"
		else:
			print subdir + ": ERROR"
	
	return(trainDict, testDict)

###################################
# SKRIPT ##########################
###################################

(trainDict, testDict) = divide();

globalIndex = libGeneral.readDictionaryFromDisk(GLOBAL_INDEX)

DATABASE_NAME = "ex4.db"
connection = sqlite3.connect(DATABASE_NAME)

######################
resultDictionary = {}
for className in testDict:
	fileList = testDict[className]
	for filename in fileList:
		
	wordVector = libGeneral.createWordVector(TEST_PATH + testFile)	
	
	#probs = bayes_classifier.classify(wordVector)
	
	probs = kNN_classifier.classify(wordVector,7)
	resultDictionary[testFile] = probs[0]
	
	print probs
	print "##########"

libGeneral.writeDictionaryToDisk(resultDictionary, "classifier_test_result.txt")
'''
