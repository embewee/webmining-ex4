import libGeneral
import os
import sqlite3
import bayes_classifier
import kNN_classifier
import codecs

######################
GLOBAL_INDEX = "globalIndex";
TRAINING_PATH = "u4_train/"
######################

globalIndex = libGeneral.readDictionaryFromDisk(GLOBAL_INDEX)
DATABASE_NAME = "ex4.db"
connection = sqlite3.connect(DATABASE_NAME)

def printMatrix(matrix):
	for row in matrix:
		print row

###################################
# SKRIPT ##########################
###################################

dirList = os.listdir(TRAINING_PATH)
nrOfClasses = len(dirList)

dictClassToIndex = {}
index = 0
for className in dirList:
	dictClassToIndex[className] = index
	index += 1

# Creates a list containing nrOfClasses lists initialized to 0
# Matrix [row][col]
matrix = [[0 for x in xrange(nrOfClasses)] for x in xrange(nrOfClasses)] 

#reverse mapping
dictIndexToClass = dict(map(lambda item: (item[1],item[0]),dictClassToIndex.items()))

print "Classifying..."

for i in range (0, nrOfClasses):
	realClass = dictIndexToClass[i]
	print "Real class name: " + realClass
	cursor = connection.cursor()
	values = [realClass,]
	sql = "SELECT FILENAME, WORD_VECTOR FROM TRAINING WHERE CLASS LIKE ? AND FOR_TESTING = 1;"
	cursor.execute(sql, values)
	
	for row in cursor.fetchall():
		fileName = row[0]
		print "   " + fileName
		wordVector = libGeneral.makeDictionaryFromString(row[1])
		probs = kNN_classifier.classify(wordVector,5)
		#probs = bayes_classifier.classify(wordVector)
		estimatedClass =  probs[0]
		print "   " + estimatedClass
		#matrix[estimated][real] 
		matrix[dictClassToIndex[estimatedClass]][i] += 1
		printMatrix(matrix) 
	
	print "#################"

# Write results to file
outputFile = codecs.open("MATRIX-knn5.txt", 'w', encoding="utf-8")
outputFile.write("v estimated class, > real class")

for i in range (0, nrOfClasses) :
	outputFile.write(str(i) + "=" + unicode(dictIndexToClass[i]) + '\n')
	
for row in matrix:
	line = ""
	for element in row:
		line = line + str(element) + ";"
	outputFile.write(line + '\n')

outputFile.close()

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
