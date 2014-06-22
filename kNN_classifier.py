import sqlite3
import math
import libGeneral

'''
Implementation of the nearest Neighbor classifier
'''
DATABASE_NAME = "ex4.db"
connection = sqlite3.connect(DATABASE_NAME)

def classify(classifyVector,n):
    cursor = connection.cursor()
    sql = "SELECT ID, WORD_VECTOR, CLASS FROM TRAINING;"
    resultDictionary = {}
    id_class_dictionary = {}
    kNNDictionary = {}
    
    cursor.execute(sql)
    for row in cursor.fetchall():
        id = row[0]
        databaseVector = libGeneral.makeDictionaryFromString(row[1])
        classname = row[2]
        
        id_class_dictionary[id] = classname
        
        databaseVector = libGeneral.normalizeDictionary(databaseVector)
        classifyVector = libGeneral.normalizeDictionary(classifyVector)
        
        sum = 0.0
        
        for key in databaseVector.keys():
            if key in classifyVector.keys():
                classifyValue = classifyVector[key]
                trainingValue = databaseVector[key]
                
                sum += math.fabs(classifyValue - trainingValue)
            else:
                sum += databaseVector[key]
                
        for key in classifyVector.keys():
            if key not in databaseVector.keys():
                sum += classifyVector[key]
                
        resultDictionary[id] = sum
    
    lowestValuesDictionary = libGeneral.getLowestValues(resultDictionary,n)
    for key in lowestValuesDictionary.keys():
        classname = id_class_dictionary[key]
        if classname not in kNNDictionary.keys():
            kNNDictionary[classname] = 1
        else:
            kNNDictionary[classname] += 1
            
    maxValue = libGeneral.getMaxValueFromDictionary(kNNDictionary)
    maxKey = libGeneral.getKeyFromMaxValueFromDictionary(kNNDictionary)
    
    return [maxKey, maxValue]
    
