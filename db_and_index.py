#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Main function of the program
'''
import os
import libGeneral
import sqlite3

######################
DATABASE_NAME = "ex4.db"
TRAIN_PATH = "u4_train/"

#######################
# Connect to Database #
try:
	connection = sqlite3.connect(DATABASE_NAME)
except:
	libGeneral.createSQLiteDB(DATABASE_NAME)
	connection = sqlite3.connect(DATABASE_NAME)
#######################

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
		
##########################
### Reading data done! ###
##########################
def createGlobalIndex(connection):
	globalIndex = libGeneral.createGlobalIndexDictionary(connection)
	libGeneral.writeDictionaryToDisk(globalIndex, "globalIndex")

########################################
### Calculating relative probability ###
########################################
def calculateRelativeProbability(connection):
	cursor = connection.cursor()
	sql = "SELECT DISTINCT CLASS FROM TRAINING;"
	cursor.execute(sql)
	for row in cursor.fetchall():
		classname = row[0]
		cursor2 = connection.cursor()
		sql = "SELECT WORD_VECTOR FROM TRAINING WHERE CLASS = ?:"
		values = [classname,]
		cursor2.execute(sql, values)
		
		classDictionary = {}
		
		for row in cursor2.fetchall():
			currentWordVector = row[0]
			currentWordVector = libGeneral.makeDictionaryFromString(currentWordVector)
			
			for key in currentWordVector:
				if key not in classDictionary.keys():
					classDictionary[key] = currentWordVector[key]
				else:
					classDictionary[key] += currentWordVector[key]
				
		