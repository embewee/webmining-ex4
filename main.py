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
######################

libGeneral.createSQLiteDB(DATABASE_NAME)

'''
Gibt ein Dictionary Verzeichnis -> Dateiliste zurueck vom uebergebenen Pfad zurueck
'''
def getTrainingFileNames(path):
	trainingFiles = {}
	dirList = os.listdir(path)
	for d in dirList:
		fileList = os.listdir(path + d)
		trainingFiles[d] = fileList
	return trainingFiles
	 
trainingFiles = getTrainingFileNames(TRAIN_PATH)

for className in trainingFiles:
	fileList = trainingFiles[className]
	for fileName in fileList:
		libGeneral.readFileToDB(fileName, TRAIN_PATH + "/" + className + "/", DATABASE_NAME, className)
		



