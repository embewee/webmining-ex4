import libGeneral
import sqlite3
import math
##############################
DATABASE_NAME = "ex4.db"
TEST_PATH = "u4_test/"
GLOBAL_INDEX = "globalIndex";
RELPROB_PATH = "bayes_model/";
connection = sqlite3.connect(DATABASE_NAME)
classes = libGeneral.determineClasses(connection)
aPrioriDictionary = libGeneral.calculateAPrioriDictionary(connection)
##############################

'''
Klassifiziert einen gegebenen Word_Vector. 
Der Word_Vector soll im Format:
    key:Wort 
    value:Haeufigkeit 
vorliegen.

Zurueckgegeben wird ein Array mit Klassenname:Wahrscheinlichkeit

Bspw.

Mystery, 0.5

Was bedeutet, dass die wahrscheinlichste Klasse "Mystery" mit einer Wahrscheinlichkeit von 50% ist.
'''
def classify(wordVector):
    
    probs = {}
    for className in classes:
        
        classProb = aPrioriDictionary[className]
        
        prob = classifyWordVectorForClass(wordVector, className, classProb)
        probs[className] = prob
    
    'Normalize the dictionary'
    probs = libGeneral.normalizeDictionary(probs)
    
    maxKey = libGeneral.getKeyFromMaxValueFromDictionary(probs)
    maxValue = libGeneral.getMaxValueFromDictionary(probs)
    
    return [maxKey, maxValue]

def classifyWordVectorForClass(testWordVector,className,classProb):
    
    trainedVector = libGeneral.readDictionaryFromDisk(RELPROB_PATH + className)
    
    #score = 1.0
    logScore = 0.0
    for key in testWordVector:
        if key in trainedVector.keys():
            # p(d|c)
            #score *= math.pow(float(trainedVector[key]), float(testWordVector[key]))
            try:
                aPriori = classProb
                part1 = math.pow(float(trainedVector[key]), float(testWordVector[key]))                
                part2 = float(aPriori)
                logScore -= math.log(part1 * part2)
            except:
                pass
            
            #print logScore
    return logScore

def calculateModel(TFIDF):

    cursor = connection.cursor()
    sql = "SELECT DISTINCT CLASS FROM TRAINING;"
    cursor.execute(sql)
    for row in cursor.fetchall():
        
        classname = row[0]
        cursor2 = connection.cursor()
        sql = "SELECT WORD_VECTOR FROM TRAINING WHERE CLASS = ?;"
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
        
        if TFIDF:
            classDictionary = libGeneral.calculateTfIdfVector(classDictionary, connection, classname)

        classDictionary = libGeneral.normalizeDictionary(classDictionary)

        libGeneral.writeDictionaryToDisk(classDictionary, "bayes_model/" + classname)
        
        print "Model: " + classname + " ::: DONE!"