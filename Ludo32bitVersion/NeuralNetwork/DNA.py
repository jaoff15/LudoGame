
import random
import math
import csv
import config
import NeuralNetwork as NN

def expectedDnaLength(noInput, noHidden, noHiddenLayers, noOutput):
    requestedLength = noInput + noInput  # Input Layer
    requestedLength += noInput * noHidden + (noHidden)  # First hidden layer
    requestedLength += (noHiddenLayers - 1) * noHidden * noHidden + ((noHiddenLayers - 1) * noHidden)  # Rest of the hidden layers
    requestedLength += noOutput * noHidden + (noOutput)  # Output Layer
    return requestedLength

class DNA:
    def __init__(self):
        self.mutationRate = 0.005

    def extractFromDNA(self, DNA, noInput, noHidden, noHiddenLayers, noOutput):
        if config.ENABLE_CHECKS:
            requestedLength = expectedDnaLength(noInput, noHidden, noHiddenLayers, noOutput)
            assert requestedLength == len(DNA), "DNA and requested lengths are not equal"
        nxtIndex = 0

        # Input layer
        wInput = DNA[nxtIndex:nxtIndex+noInput]
        nxtIndex += noInput
        wBiasInput = DNA[nxtIndex:nxtIndex + noInput]
        nxtIndex += noInput

        wHidden = []
        wBiasHidden = []

        # First hidden layer
        wHidden.extend(DNA[nxtIndex:nxtIndex + noInput*noHidden])
        nxtIndex += noInput*noHidden
        wBiasHidden.extend(DNA[nxtIndex:nxtIndex + noHidden])
        nxtIndex += noHidden

        # Rest of the hidden layers
        for h in range(1,noHiddenLayers):
            wHidden.extend(DNA[nxtIndex:nxtIndex + noHidden*noHidden])
            nxtIndex += noHidden*noHidden

            wBiasHidden.extend(DNA[nxtIndex:nxtIndex + noHidden])
            nxtIndex += noHidden

        wOutput = DNA[nxtIndex:nxtIndex + noHidden*noOutput]
        nxtIndex += noHidden*noOutput

        wBiasOutput = DNA[nxtIndex:nxtIndex + noOutput]
        nxtIndex += noOutput

        if config.ENABLE_CHECKS:
            buildLength = len(wInput) + len(wBiasInput)  + len(wOutput) + len(wBiasOutput)+ len(wHidden) + len(wBiasHidden)

            assert buildLength == len(DNA), "DNA and build lengths are not equal"

        return wInput, wBiasInput, wHidden, wBiasHidden, wOutput, wBiasOutput

    def mutateDNA(self, DNA):
        mutations = math.floor(len(DNA) * self.mutationRate)
        for i in range(0, mutations):
            randId = random.randrange(0,len(DNA))
            DNA[randId] = random.random()
        return DNA

    def combineDNA(self, DNA1, DNA2):
        newDNA = []
        for i in range(0, len(DNA1), 10):
            if random.random() < 0.5:
                newDNA.extend(DNA1[i:i+10])
            else:
                newDNA.extend(DNA2[i:i+10])
        assert len(newDNA) == len(DNA1), "New DNA constructed wrong"
        return newDNA

    def getDNA(self, NN):
        wInput      = NN.getInputWeights()
        wBiasInput  = NN.getInputBiasWeights()
        wHidden     = NN.getHiddenWeights()
        wBiasHidden = NN.getHiddenBiasWeights()
        wOutput     = NN.getOutputWeights()
        wBiasOutput = NN.getOutputBiasWeights()
        return wInput + wBiasInput + wHidden + wBiasHidden + wOutput + wBiasOutput


def toStr(DNA):
    dnaStr = "\n".join([str(elem) for elem in DNA], )
    return dnaStr

def fromStr(dnaStr):
    reader = csv.reader(dnaStr, delimiter='\n')
    DNA = []
    for row in reader:
        DNA.append(row[0][0])
    return DNA
