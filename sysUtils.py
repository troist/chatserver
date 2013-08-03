#! /usr/bin/env python
##########################################
# 2013-05-21
# sysUtils
# v2.0.4
##########################################
# alex.jones@mkodo.com
##########################################
# Imports

import sys
import os

##########################################

flagList = []

def arrayInsert(targetArray, indexValue, checkIfValExists):
    '''Inputs a value into an array. Checks if the index exists in the array before appending'''
    arrayIndex = getIndex(targetArray, indexValue)
    if (arrayIndex == -1 and checkIfValExists) or (not checkIfValExists):
        targetArray.append([indexValue])
    return targetArray

def getIndex(searchArray, searchString):
    '''Searches through an array, checking values at i[0] for a match, if it finds one with return the index of i. Used for finding subArrays in an Array, relevant to how I store data'''
    returnIndex = -1
    for i in searchArray:
        if len(i) > 0:
            if i[0] == searchString:
                returnIndex = searchArray.index(i)
    return returnIndex

def readInFile(target):
    '''Return lines from inside a file'''
    f = open(target, 'r')
    rawData = f.readlines()
    f.close()
    if rawData == []:
        return ""
    else:
        return rawData[0]

def checkIfFileExists(target):
    return os.path.isfile(target)

def writeToFile(target, fileContents):
    '''Write string to file'''
    f = open(target, 'w')
    f.write(fileContents)
    f.close()

def getFileList(location):
    '''Returns a list of files from the given location. Hidden files will be ignored. Any further args will be treated as strings that '''
    if os.path.isfile(location):
        return [location]
    else:
        rawFileList   = os.listdir(location)
        cleanFileList = []
        criteria = -1
        if checkFlag('F') != -1:
            if len(getFlagBody('F')) > 0:
                criteria = getFlagBody('F').split('%20')
        for i in rawFileList:
            if i[:1] != '.':
                matched = True
                if criteria != -1:
                    for j in criteria:
                        if i.find(str(j)) == -1:
                            matched = False
                if location != '.' and matched:
                    if location[-1:] != '/':
                        cleanFileList.append(location + '/' + i)
                    else:
                        cleanFileList.append(location + i)
                else:
                    if matched:
                        cleanFileList.append(i)
        return sorted(cleanFileList)

def stripJson(stringToStrip):
    '''Strips escaped characters off the front of a string - assumes an escaped character looks like "%xx" Returns the stripped string plus the offSet caused (int)'''
    offSet = 0
    if stringToStrip[:1] == '%':
        while stringToStrip[:1] == '%':
            stringToStrip = stringToStrip[3:]
            offSet += 3
    return [stringToStrip, offSet]

def printSysArgs():
    '''Prints out the SysArgs in a list with an index'''
    counter = 0
    for i in sys.argv:
        vPrint(str(counter) + ' = ' + i)
        counter += 1

def setFlags():
    '''Takes the system args and splits them into flags and gives the flagBody as the space between the flags'''
    global flagList
    rawArgs   = sys.argv[1:]
    flagList  = []
    if len(rawArgs) != 0:
        for i in rawArgs:
            i.replace('"','')
            if i[:1] == '-' and len(i) == 1:
                continue
            elif i[:1] == '-' and len(i) >= 2:
                actualFlag = i[1:2]
                if len(i) == 2:
                    flagList.append([actualFlag,[]])
                else:
                    flagList.append([actualFlag,[i[2:]]])
            else:
                if len(flagList) == 0:
                    pass
                else:
                    if len(flagList[-1][1]) == 0:
                        flagList[-1][1].append(str(i))
                    else:
                        flagList[-1][1][0] += '%20' + str(i)

def getFlagList():
    return flagList

def checkFlag(flagToCheck):
    '''Checks a given flag against the flagList. If the flag exists, it will return the index, else will return -1'''
    index = -1
    for i in flagList:
        if i[0] == flagToCheck:
            index = flagList.index(i)
            break
    return index

def getFlagBody(flagToGet):
    '''Checks a given flag exists using checkFlag. Uses the index returned to find the body, using flagList[index][1][0]'''
    flagIndex = checkFlag(flagToGet)
    flagBody = -1
    if flagIndex != -1 and len(flagList[flagIndex][1]) >= 1:
        flagBody = flagList[flagIndex][1][0]
    return flagBody

def updateFlagBody(flagToUpdate, dataToInsert):
    global flagList
    if checkFlag(flagToUpdate) != -1:
        flagList[checkFlag(flagToUpdate)][1][0] = dataToInsert
    else:
        flagList.append([flagToUpdate,[dataToInsert]])

def vPrint(itemToPrint):
    '''Verbose Print, only prints if the 'v' flag is active'''
    if checkFlag('v') != -1:
        print itemToPrint

def getLocation():
    location = -1
    if sys.argv[0][:1] == '.':
        if os.getcwd()[-1:] == '/':
            location = os.getcwd()[:-1] + sys.argv[0][1:]
        else:
            location = os.getcwd() + sys.argv[0][1:]
    else:
        location = sys.argv[0]
    location = location[:location.rfind('/') + 1]
    return location

def utilSysExit(message):
    sys.exit(message)
