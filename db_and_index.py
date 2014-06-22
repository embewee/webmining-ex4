#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Main function of the program
'''
import os
import libGeneral
import sqlite3
#import bayes_classifier

######################
DATABASE_NAME = "ex4.db"
TRAIN_PATH = "u4_train/"
TEST_PATH = "u4_test/"
GLOBAL_INDEX = "globalIndex";
RELPROB_PATH = "bayes_model/";
######################

'''
Gibt ein Dictionary Verzeichnis -> Dateiliste zurueck vom uebergebenen Pfad zurueck
'''
def getFileDict(path):
	trainingFiles = {}
	dirList = os.listdir(path)
	for d in dirList:
		fileList = os.listdir(path + d)
		trainingFiles[d] = fileList
	return trainingFiles

def readAllFilesToDB(connection):
	trainingFiles = getFileDict(TRAIN_PATH)
	
	for className in trainingFiles:
		fileList = trainingFiles[className]
		for fileName in fileList:
			libGeneral.readFileToDB(fileName, TRAIN_PATH + "/" + className + "/", connection, className)
			
	connection.commit()

def createGlobalIndex(connection):
	globalIndex = libGeneral.createGlobalIndexDictionary(connection)
	libGeneral.writeDictionaryToDisk(globalIndex, "globalIndex")
		
##########################
#libGeneral.createSQLiteDB(DATABASE_NAME)
#print "Created database."

connection = sqlite3.connect(DATABASE_NAME)
print "Connected to database."
#######################

#readAllFilesToDB(connection)
#print "Read all files to database."

#createGlobalIndex(connection)
#print "Created global index."

#bayes_classifier.calculateModel(True)
#print "Calculated bayes model"
