#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import sqlite3
import operator
import extractor
import codecs
import math

'''
Removes special characters like '\n', '\s' etc from a given string

INPUT:
s:        the string to remove the characters from

OUTPUT:
s:        the string without special characters
'''
def removeSpecialCharacters(s):
    # Remove all characters except for the given ones
    uRet = re.sub(u'[^A-Za-z äüÖÄÜßêéèáíóúñ]+', ' ', s)
    return uRet

'''
Removes additional spaces in a string
The returned string only has single spaces
'''
def removeAdditionalSpaces(s):
    return re.sub('[ +]+', ' ', s)
    
'''
Makes a given string all lower case with special german characters
'''
def makeStringLowerCase(s):
    s = s.lower()
    s = s.replace(u'Ü', u'ü')
    s = s.replace(u'Ä', u'ä')
    s = s.replace(u'Ö', u'ö')
    return s

'''
Creates the database needed for the task.

If database already exists, it will be deleted!
'''
def createSQLiteDB(db):
    # Remove old database
    if os.path.isfile(db):
        os.remove(db)
    
    db_connection = sqlite3.connect(db)
    db_connection.execute('''CREATE TABLE TRAINING
           (
           ID                INTEGER PRIMARY KEY AUTOINCREMENT,
           WORD_VECTOR       TEXT,
           CLASS             TEXT    NOT NULL
           );''')
    db_connection.close()
    
'''
Make a csv string from a localDictionary
    key;value
    
Lines are separated by '\n'
'''
def makeStringFromDictionary(localDictionary):
    outputString = u""
    for key in localDictionary.keys():
        if outputString == "":
            outputString = key + u";" + unicode(localDictionary[key])
        else:
            outputString = outputString + u"\n" + key + u";" + unicode(localDictionary[key])
        
    return outputString

def makeDictionaryFromString(dicString):
    outputDict = {}
    dicList = dicString.split("\n")
    for line in dicList:
        if line == "": 
            continue
        splitLine = line.split(";")
        key = splitLine[0]
        value = splitLine[1]
        
        if value == "":
            continue
        outputDict[key] = float(value)
        
    return outputDict

'''
Calculates the sum of all values in the localDictionary
'''
def getDictionarySum(localDictionary):
    sum = 0.0
    for key in localDictionary.keys():
        sum += localDictionary[key]
    return sum

'''
Calculates the sum of all values and divides every value with that sum.
Returns the normalized localDictionary.
'''
def normalizeDictionary(localDictionary):
    sum = getDictionarySum(localDictionary)
    for key in localDictionary.keys():
        localDictionary[key] = localDictionary[key] / sum
    return localDictionary

'''
Returns a localDictionary with the n keys with highest value

INPUT:
    localDictionary - the localDictionary to get the values from
    n - the n highest values that should be returned
    
OUTPUT:
    outputDictionary - a localDictionary containing the n highest values
'''
def getHighestValues(localDictionary, n):
    outputDictionary = {}
    sorted_keywords = sorted(localDictionary.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    dicLen = len(sorted_keywords)
    if n > dicLen:
        n = dicLen
    
    x = 0
    while x < n:
        key = sorted_keywords[x]
        outputDictionary[key[0]] = localDictionary[key[0]]
        x += 1
    return outputDictionary

def getLowestValues(localDictionary, n):
    outputDictionary = {}
    sorted_keywords = sorted(localDictionary.iteritems(), key=operator.itemgetter(1), reverse=False)
    
    dicLen = len(sorted_keywords)
    if n > dicLen:
        n = dicLen
    
    x = 0
    while x < n:
        key = sorted_keywords[x]
        outputDictionary[key[0]] = localDictionary[key[0]]
        x += 1
    return outputDictionary

def createWordVector(absFilename):
    inputFile = codecs.open(absFilename, "r", "utf-8")
    inputString = inputFile.read()
    
    # Get the wordlist, remove stopwords and stem the words
    inputString = removeSpecialCharacters(inputString)
    inputString = removeAdditionalSpaces(inputString)
    inputString = makeStringLowerCase(inputString)
    
    wordList = inputString.split()
    wordList = removeSingleCharacters(wordList)
    wordList = extractor.removeStopwords(wordList, "english")    
    wordList = extractor.stemList(wordList)
    
    wordVector = makeDictionaryFromList(wordList)
    
    return wordVector

'''
Reads a given html file to the DB
'''
def readFileToDB(filename, path, connection, docClass):
    
    cursor = connection.cursor()
    
    filename = unicode(filename)
    absFilename = path + filename
    
    wordVector = createWordVector(absFilename)
    
    # If the word list is empty
    # Dont write list to Database
    if len(wordVector.keys()) == 0:
        print "ERROR reading file : " + absFilename
        return

    # Write data to database
    serializedDictionary = makeStringFromDictionary(wordVector)
    values = (serializedDictionary, docClass)
    sql = "INSERT INTO TRAINING (WORD_VECTOR, CLASS) VALUES (?,?);"
    cursor.execute(sql, values)
    
'''
Calculate the global dictionary from all files in DB
'''
def calculateIDFVector(connection, docClass):
    
    values = [docClass,]
    sql = "SELECT WORD_VECTOR FROM TRAINING WHERE CLASS = ?;"
    selectCursor = connection.execute(sql, values)
    idfVector = {}
    rows = selectCursor.fetchall()
        
    for row in rows:
        #url = row[0]
        serializedDictionary = row[0]
        #docClass = row[3]
        #idD = row[4]

        loadedDictionary = makeDictionaryFromString(serializedDictionary)
        for key in loadedDictionary:
            if not key in idfVector.keys():
                idfVector[key] = 1.0
            else:
                idfVector[key] += 1.0
    
    for key in idfVector:
        rowLength = len(rows)
        idfVector[key] =  math.log(float(rowLength)/idfVector[key],10)
    
    return idfVector

'''
Max value from dictionary
'''
def getMaxValueFromDictionary(dictionary):

    try:
        b = dict(map(lambda item: (item[1],item[0]),dictionary.items()))
        keys = b.keys()
        maxValue = max(keys)
        return maxValue
    except:
        return 0.0
    
def getKeyFromMaxValueFromDictionary(dictionary):

    try:
        b = dict(map(lambda item: (item[1],item[0]),dictionary.items()))
        keys = b.keys()
        maxValue = max(keys)
        key = b[maxValue]
        return key
    except:
        return ""

'''
Creates a global index dictionary from a given database connection

OUTPUT:
    key=word:value=index
    
'''
def createGlobalIndexDictionary(connection):

    indexDict = {}
    index = 1
    
    sql = "SELECT * FROM TRAINING WHERE 1;"
    selectCursor = connection.execute(sql)
    rows = selectCursor.fetchall()
    
    for row in rows:
        serializedDictionary = row[1]
        loadedDictionary = {}
        loadedDictionary = makeDictionaryFromString(serializedDictionary)
        
        for key in loadedDictionary:
            if not key in indexDict.keys():
                indexDict[key] = index
                index += 1
                            
    return indexDict
    
'''
Writes the given dictionary to specified file

INPUT:
    dictionary - the dictionary containing key and value. Note that key should be UTF-8 encoded
    fileName - the filename to write the dictionary to the disk to. The file will be saved in current working directory
'''
def writeDictionaryToDisk(dictionary, fileName):
    # save the results to file named results_"document_filename".txt
    outputFile = codecs.open(fileName, 'w', encoding="utf-8")

    sorted_keywords = sorted(dictionary.iteritems(), key=operator.itemgetter(1))
    for word_tuple in sorted_keywords:
        line = word_tuple[0] + ";" + unicode(dictionary[word_tuple[0]]) +'\n'
        outputFile.write(line)
    
    outputFile.close()

'''
Reads the given file into a dictionary

INPUT:
    fileName - the filename to read from
'''
def readDictionaryFromDisk(fileName):
	inputFile = codecs.open(fileName, 'r', encoding="utf-8")
	string = inputFile.read()
	return makeDictionaryFromString(string)
        
'''
Updates the database by filtering the n most common words
'''
def updateMostCommonWords(DATABASE_NAME, docClass, n, testing=0):
    connection = sqlite3.connect(DATABASE_NAME)
    values = [docClass,]
    sql = "SELECT * FROM TRAINING WHERE CLASS = ?;"
    selectCursor = connection.execute(sql, values)
    rows = selectCursor.fetchall()
    
    mostCommonWordsDictionary = {}
    
    for row in rows:
        originalWordVectorString = row[5]
        originalWordVector = makeDictionaryFromString(originalWordVectorString)
        
        for key in originalWordVector.keys():
            if not key in mostCommonWordsDictionary.keys():
                mostCommonWordsDictionary[key] = originalWordVector[key]
            else:
                mostCommonWordsDictionary[key] += originalWordVector[key]
        
    mostCommonWordsDictionary = getHighestValues(mostCommonWordsDictionary, n)
    print mostCommonWordsDictionary
    
    for row in rows:
        idD = row[4]
        originalWordVectorString = row[5]
        originalWordVector = makeDictionaryFromString(originalWordVectorString)
        
        newWordVector = {}
        
        for key in originalWordVector.keys():
            if key in mostCommonWordsDictionary.keys():
                newWordVector[key] = originalWordVector[key]
        
        if len(newWordVector) == 0:
            pass
        
        if(testing):
            newWordVector = originalWordVector
        
        newWordVectorString = makeStringFromDictionary(newWordVector)
        values = (newWordVectorString, idD)
        sql = "UPDATE TRAINING SET WORD_VECTOR = ? WHERE ID = ?"
        connection.execute(sql, values)
        #connection.commit()
        
    connection.commit()       

'''
Removes single characters from a given list
'''
def removeSingleCharacters(wordList):
    for word in wordList:
        if len(word) == 1:
            wordList.remove(word)
    
    return wordList

def makeDictionaryFromList(wordList):
    
    dictionary = {}
    for word in wordList:
        if word not in dictionary.keys():
            dictionary[word] = 1.0
        else:
            dictionary[word] += 1.0
            
    return dictionary

def determineClasses(connection):
    classes = []
    cursor = connection.cursor()
    sql = "SELECT DISTINCT CLASS FROM TRAINING;"
    cursor.execute(sql)
    for row in cursor.fetchall():
        className = row[0]
        classes.append(className)
        
    return classes

def calculateTfIdfVector(dictionary, connection, className):
    
    idf_vector = calculateIDFVector(connection, className)
    
    maximumValue = getMaxValueFromDictionary(dictionary)
            
    tf_idf_dictionary = {}
    for key in dictionary:
        tf_idf_dictionary[key] = float(dictionary[key]/maximumValue) * float(idf_vector[key])
        
    return tf_idf_dictionary

def calculateAPrioriDictionary(connection):
    cursor = connection.cursor()
    sql = "SELECT CLASS, COUNT(CLASS) FROM TRAINING GROUP BY CLASS;"
    cursor.execute(sql)
    aPrioriDict = {}
    for row in cursor.fetchall():
        className = row[0]
        freq = row[1]
        
        aPrioriDict[className] = freq
    
    aPrioriDict = normalizeDictionary(aPrioriDict)
    return aPrioriDict