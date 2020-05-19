
# import os.path
from os import path
import os

gFileFolder = "data"
gFileFolderNumber = None

def _findFolderNumber():
    for i in range(0, 1000):
        if not path.isdir(gFileFolder + '/' + str(i)):
            os.mkdir(gFileFolder +'/'+str(i))
            print("Using folder: "+str(i))
            return str(i)
    assert False, "File creation failed"

def makeNewFile(file):
    global gFileFolder
    global gFileFolderNumber
    if gFileFolderNumber == None:
        gFileFolderNumber = _findFolderNumber()
    return gFileFolder + '/' + gFileFolderNumber + '/' + file

def appendToFile(file, lineStr=""):
    with open(file, "a") as f:
        f.write(lineStr + "\n")

def appendListToFile(file, start, l):
    data = start
    for i in range(0, len(l)):
        data += ", " + str(l[i])
    appendToFile(file, data)

def writeToFile(file, data=""):
    with open(file, "w") as f:
        f.write(data)
