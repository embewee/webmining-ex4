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


def extract(htmlFile):
    '''
    Extracts the content from a html file.
    Extractor will ignore links, images and emphasis. 
    E-Mail Adresses will be removed.
    Result will be free of special characters, multi spaces and single character words.
    Result will lower case

    INPUT:
        htmlFile - A string containing a html file

    OUTPUT:
        wordList - A list of words that are contained in the htmlFile
    '''
        
    # Create the extractor object
    # and set the properties
    htmlExtractor = html2text.HTML2Text()
    htmlExtractor.ignore_links = True
    htmlExtractor.ignore_images = True
    htmlExtractor.ignore_emphasis = True
    
    htmlContent = htmlExtractor.handle(htmlFile)
    
    # Regex for finding e-mail adresses
    regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                        "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                        "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
    emailList = re.findall(regex, htmlContent)
    for email in emailList:
        htmlContent = htmlContent.replace(email[0], "")
    
    # Remove special characters
    # Remove additional spaces
    # Make string lower case
    htmlContent = libGeneral.removeSpecialCharacters(htmlContent)
    htmlContent = libGeneral.removeAdditionalSpaces(htmlContent)
    htmlContent = libGeneral.makeStringLowerCase(htmlContent)
    
    wordList = htmlContent.split()
    # Remove single characters
    wordList = removeSingleCharacters(wordList)
    
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