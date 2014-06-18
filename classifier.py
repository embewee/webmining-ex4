import libGeneral
import os
import sqlite3

######################
DATABASE_NAME = "ex4.db"
TEST_PATH = "u4_test/"
GLOBAL_INDEX = "globalIndex";
RELPROB_PATH = "bayes_model/";
######################

# FUNKTIONEN 

def classifyWordVectorForClass(c, wordVector):
	trainedVector = 
	for word in wordVector:
		print word

'''
Input:  WordVector wort->Hauefigkeite
Output: Vector mit Wahrscheinlichkeiten der Zugehoerigkeiten zu einer Klasse
'''
def classify(wordVector):
	probs = {}
	for c in classes:
		prob = classifyWordVectorForClass(c, wordVector)
		probs[c] = prob
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


for testFile in testFiles:
	wordVector = libGeneral.createWordVector(TEST_PATH + testFile)
	classify(wordVector)
