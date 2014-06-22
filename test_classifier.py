import libGeneral
import os
import bayes_classifier
import kNN_classifier

######################
GLOBAL_INDEX = "globalIndex";

#Wenn in einem Ordner die Unterordner train/
TEST_PATH = "u4_eval/"
######################

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

libGeneral.writeDictionaryToDisk(resultDictionary, "classifier_test_result.txt")
