import libGeneral
import os
import sqlite3
import math

######################
DATABASE_NAME = "ex4.db"
TEST_PATH = "u4_test/"
GLOBAL_INDEX = "globalIndex";
RELPROB_PATH = "bayes_model/";
######################

# FUNKTIONEN 

def classifyWordVectorForClass(className, testWordVector):
	trainedVector = readDictionaryFromDisk(RELPROB_PATH + className)
	score = 1.0
	for key in testWordVector:
		if key in trainedVector.keys():
			# p(d|c)
			score *= math.pow(trainedVector[key], testWordVector[key])
	return score

'''
Input:  WordVector wort->Hauefigkeite
Output: Vector mit Wahrscheinlichkeiten der Zugehoerigkeiten zu einer Klasse
'''
def classify(wordVector):
	probs = {}
	for className in classes:
		prob = classifyWordVectorForClass(className, wordVector)
		probs[className] = prob
	return probs





##############################################################

# SKRIPT

connection = sqlite3.connect(DATABASE_NAME)

testFiles = os.listdir(TEST_PATH)

globalIndex = libGeneral.readDictionaryFromDisk(GLOBAL_INDEX)

classes = []
classProbVectors = {}

cursor = connection.cursor()
sql = "SELECT DISTINCT CLASS FROM TRAINING;"
cursor.execute(sql)
for row in cursor.fetchall():
	className = row[0]
	classes.append(className)
	classProbVector = libGeneral.readDictionaryFromDisk(RELPROB_PATH + className)
	classProbVectors[className] = classProbVector


wordVector = libGeneral.createWordVector("testdoc.txt")
probs = classify(wordVector)
print probs

'''
for testFile in testFiles:
	wordVector = libGeneral.createWordVector(TEST_PATH + testFile)
	probs = classify(wordVector)
	print testFile
	print probs
	print "##########"
'''
