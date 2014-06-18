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
	trainedVector = libGeneral.readDictionaryFromDisk(RELPROB_PATH + className)
	#score = 1.0
	logScore = 0.0
	for key in testWordVector:
		if key in trainedVector.keys():
			# p(d|c)
			#score *= math.pow(float(trainedVector[key]), float(testWordVector[key]))
			aPriori = aPrioriDict[className]
			try:
				logScore -= math.log(float(aPriori) * math.pow(float(trainedVector[key]), float(testWordVector[key])))
			except:
				pass
			#print logScore
	return logScore

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



cursor = connection.cursor()
sql = "SELECT CLASS, COUNT(CLASS) FROM TRAINING GROUP BY CLASS;"
cursor.execute(sql)
aPrioriDict = {}
for row in cursor.fetchall():
	className = row[0]
	freq = row[1]
	aPrioriDict[className] = freq
aPrioriDict = libGeneral.normalizeDictionary(aPrioriDict)
print aPrioriDict
'''
wordVector = libGeneral.createWordVector("testdoc.txt")
probs = classify(wordVector)
print probs
estimatedClass = libGeneral.getKeyFromMaxValueFromDictionary(probs);
print estimatedClass

'''
for testFile in testFiles:
	wordVector = libGeneral.createWordVector(TEST_PATH + testFile)
	probs = classify(wordVector)
	print testFile
	#print probs
	estimatedClass = libGeneral.getKeyFromMaxValueFromDictionary(probs);
	print estimatedClass
	print "##########"
