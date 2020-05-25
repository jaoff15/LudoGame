from os import path
import os

folderNumber = 151

geneCount = 9

file = "F:/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/" + str(folderNumber)+"/weights.csv"
prettyFile = "F:/Dropbox/3rd Semester Master/Tools of Artificial Intelligence/LudoGame/Ludo64bitVersion/data/" + str(folderNumber)+"/weights_pretty.csv"

data = []
with open(file, "r") as f:
    data = f.read()
data = data.split(' ')
data = ' '.join(data).split()
data = data[1:]
data[-1] = data[-1][:-1]

header = 'Piece, Out from home, hit goal, Knock home, Move to less dangerous area, Move within knocking distance, Move to more dangerous area, Bounce off goal, Piece order, Bias\n'
with open(prettyFile, "w") as f:
    f.write(header)
    for i in range(0,4):
        line = ''+str(i)
        for j in range(0, geneCount):
            # print("i: %s, j: %s" % (i,j))
            # print(i*geneCount+j)
            line += ',' + data[i*geneCount+j]
        line += '\n'
        f.write(line)