import libGeneral
import os
import sqlite3
import math
import bayes_classifier
import kNN_classifier

######################
DATABASE_NAME = "ex4.db"
TEST_PATH = "u4_test/"
GLOBAL_INDEX = "globalIndex";
RELPROB_PATH = "bayes_model/";
######################

connection = sqlite3.connect(DATABASE_NAME)
testFiles = os.listdir(TEST_PATH)
globalIndex = libGeneral.readDictionaryFromDisk(GLOBAL_INDEX)

######################
resultDictionary = {}
for testFile in testFiles:
	wordVector = libGeneral.createWordVector(TEST_PATH + testFile)	
	
	#probs = bayes_classifier.classify(wordVector)
	
	probs = kNN_classifier.classify(wordVector,7)
	resultDictionary[testFile] = probs[0]
	
	print probs
	print "##########"

libGeneral.writeDictionaryToDisk(resultDictionary, "G02_predictions.txt")