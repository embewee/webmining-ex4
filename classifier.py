import libGeneral
import os
import sqlite3

######################
DATABASE_NAME = "ex4.db"
TEST_PATH = "u4_test/"
GLOBAL_INDEX = "globalIndex";
######################

def classifyForClass(c, word):
	

def classify(wordList):
	
	
	
	for c in classes:
		for word in docString:
			classifyForClass(c, word)




connection = sqlite3.connect(DATABASE_NAME)

testFiles = os.listdir(TEST_PATH)

classes = []


#for testFile in testFiles:
#	wordVector = libGeneral.createWordVector(TEST_PATH + testFile)
#	print wordVector

globalIndex = libGeneral.readDictionaryFromDisk(GLOBAL_INDEX)


cursor = connection.cursor()
sql = "SELECT DISTINCT CLASS FROM TRAINING;"
cursor.execute(sql)
for row in cursor.fetchall():
	classes.append(row[0])


