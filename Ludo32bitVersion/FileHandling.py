
# import os.path
from os import path
import os

gFileFolder = "data"
gFileFolderNumber = None

def _findFolderNumber():
    for i in range(0, 100):
        if not path.isdir(gFileFolder + '/' + str(i)):
            os.mkdir(gFileFolder +'/'+str(i))
            return str(i)

def makeNewFile(file):
    global gFileFolder
    global gFileFolderNumber
    if gFileFolderNumber == None:
        gFileFolderNumber = _findFolderNumber()
    return gFileFolder + '/' + gFileFolderNumber + '/' + file

def appendToFile(file, lineStr=""):
    with open(file, "a") as f:
        f.write(lineStr + "\n")

def writeToFile(file, data=""):
    with open(file, "w") as f:
        f.write(data)
