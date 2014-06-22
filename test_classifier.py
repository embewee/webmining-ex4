import libGeneral
import os
import sqlite3
import bayes_classifier
import kNN_classifier

######################
GLOBAL_INDEX = "globalIndex";
TRAINING_PATH = "u4_train/"
######################

globalIndex = libGeneral.readDictionaryFromDisk(GLOBAL_INDEX)
DATABASE_NAME = "ex4.db"
connection = sqlite3.connect(DATABASE_NAME)

###################################
# SKRIPT ##########################
###################################

dirList = os.listdir(TRAINING_PATH)

for realClass in dirList:
	print "Real class name: " + realClass
	cursor = connection.cursor()
	values = [realClass,]
	sql = "SELECT FILENAME, WORD_VECTOR FROM TRAINING WHERE CLASS LIKE ? AND FOR_TESTING = 1;"
	cursor.execute(sql, values)
	
	for row in cursor.fetchall():
		fileName = row[0]
		print "   " + fileName
		wordVector = libGeneral.makeDictionaryFromString(row[1])
		probs = kNN_classifier.classify(wordVector,7)
		estimatedClass =  probs[0]
		print "   " + estimatedClass
	
	print "#################"

'''
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
