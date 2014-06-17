#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Extracts the content from a html file
'''
import html2text
import libGeneral
import re
import nltk
import codecs


def extract(s):
 
    # Remove special characters
    # Remove additional spaces
    # Make string lower case
    htmlContent = libGeneral.removeSpecialCharacters(s)
    htmlContent = libGeneral.removeAdditionalSpaces(s)
    htmlContent = libGeneral.makeStringLowerCase(s)
    
    wordList = htmlContent.split()
    # Remove single characters
    # wordList = removeSingleCharacters(wordList)
    
    return wordList

'''
Remove stopwords from a given string
'''
def removeStopwords(wordList, language):
    inputFile = codecs.open("./stopwords/"+language+".txt", "r", "utf-8")
    inputString = inputFile.read()
    
    #inputString = libGeneral.removeSpecialCharacters(inputString)
    inputString = libGeneral.removeAdditionalSpaces(inputString)
    inputString = libGeneral.makeStringLowerCase(inputString)
    
    stopwordList = inputString.split()
    
    x = len(wordList) - 1
    while x > -1:
        word = wordList[x]
        if word in stopwordList:
            del wordList[x]
        x -= 1
    
    return wordList

'''
stems the given list of words
'''
def stemList(wordList):
    stemmer = nltk.stem.porter.PorterStemmer()
    outputList = []
    for word in wordList:
        outputList.append(stemmer.stem(word))
    
    return outputList

'''
Removes single characters from a given list
'''
def removeSingleCharacters(wordList):
    for word in wordList:
        if len(word) == 1:
            wordList.remove(word)
    
    return wordList