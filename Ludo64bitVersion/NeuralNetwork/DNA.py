
import random
import math
import csv
import config
import numpy as np
import NeuralNetwork as NN
from numba import jit, cuda

gDnaLength = None

def expectedDnaLength(noInput, noHidden, noHiddenLayers, noOutput):
    global gDnaLength
    # If the DNA length has not been calculated yet. Calculate it. Otherwise look it up
    if gDnaLength == None:
        r1 = noInput + noInput  # Input Layer
        r2 = noInput * noHidden + (noHidden)  # First hidden layer
        r3 = (noHiddenLayers - 1) * noHidden * noHidden + ((noHiddenLayers - 1) * noHidden)  # Rest of the hidden layers
        r4 = noOutput * noHidden + (noOutput)  # Output Layer
        gDnaLength = r1 + r2 + r3 + r4
    return gDnaLength

class DNA:
    def __init__(self):
        self.mutationRate = 0.05

    def extractFromDNA(self, DNA, noInput, noHidden, noHiddenLayers, noOutput):
        if config.ENABLE_CHECKS:
            requestedLength = expectedDnaLength(noInput, noHidden, noHiddenLayers, noOutput)
            assert requestedLength == len(DNA), "DNA and requested lengths are not equal"
        nxtIndex = 0

        # Input layer
        wInput = np.array(DNA[nxtIndex:nxtIndex+noInput])
        nxtIndex += noInput
        wBiasInput = np.array(DNA[nxtIndex:nxtIndex + noInput])
        nxtIndex += noInput

        wHidden = np.zeros(noInput*noHidden+noHidden*(noHiddenLayers-1)*noHidden)
        nxtHiddenIndex = 0
        wBiasHidden = np.zeros(noHiddenLayers*noHidden)

        # First hidden layer
        # wHidden.extend(DNA[nxtIndex:nxtIndex + noInput*noHidden])
        wHidden[nxtHiddenIndex:nxtHiddenIndex+noInput * noHidden] = (DNA[nxtIndex:nxtIndex + noInput * noHidden])
        nxtIndex += noInput*noHidden
        # wBiasHidden.extend(DNA[nxtIndex:nxtIndex + noHidden])
        wBiasHidden[nxtHiddenIndex:nxtHiddenIndex + noHidden] = (DNA[nxtIndex:nxtIndex + noHidden])
        nxtIndex += noHidden

        # Rest of the hidden layers
        for h in range(1,noHiddenLayers):
            # wHidden.extend(DNA[nxtIndex:nxtIndex + noHidden*noHidden])
            wHidden[nxtHiddenIndex:nxtHiddenIndex + noHidden * noHidden] = (DNA[nxtIndex:nxtIndex + noHidden * noHidden])
            nxtIndex += noHidden*noHidden

            # wBiasHidden.extend(DNA[nxtIndex:nxtIndex + noHidden])
            wBiasHidden[nxtHiddenIndex:nxtHiddenIndex + noHidden] = (DNA[nxtIndex:nxtIndex + noHidden])
            nxtIndex += noHidden

        wOutput = np.array(DNA[nxtIndex:nxtIndex + noHidden*noOutput])
        nxtIndex += noHidden*noOutput

        wBiasOutput = np.array(DNA[nxtIndex:nxtIndex + noOutput])
        nxtIndex += noOutput

        if config.ENABLE_CHECKS:
            buildLength = len(wInput) + len(wBiasInput)  + len(wOutput) + len(wBiasOutput)+ len(wHidden) + len(wBiasHidden)
            assert buildLength == len(DNA), "DNA and build lengths are not equal"

        return wInput, wBiasInput, wHidden, wBiasHidden, wOutput, wBiasOutput


    def mutateDNA(self, DNA):
        return _mutate(DNA, self.mutationRate)
        # mutations = math.floor(len(DNA) * self.mutationRate)
        # for i in range(0, mutations):
        #     randId = random.randrange(0,len(DNA))
        #
        #     # Version 1 - Exchange with random weight
        #     # DNA[randId] = random.random()
        #
        #     # Version 2 - Modify with weight following gaussian distribution
        #     DNA[randId] += random.gauss(0, 0.08)
        # return DNA

    def combineDNA(self, DNA1, DNA2):
        # newDNA = DNA1
        # for i in range(0, len(DNA1), 10):
        #     if random.random() < 0.5:
        #         newDNA[i:i+10] = DNA2[i:i+10]
        assert len(DNA1) == len(DNA2), "The two DNA strings should be the same length"
        newDNA = _crossover(DNA1,DNA2)
        assert len(newDNA) == len(DNA1), "New DNA constructed wrong"
        return newDNA

    def getDNA(self, NN):
        wInput      = NN.getInputWeights()
        wBiasInput  = NN.getInputBiasWeights()
        wHidden     = NN.getHiddenWeights()
        wBiasHidden = NN.getHiddenBiasWeights()
        wOutput     = NN.getOutputWeights()
        wBiasOutput = NN.getOutputBiasWeights()
        return np.concatenate((wInput, wBiasInput, wHidden, wBiasHidden, wOutput, wBiasOutput))
        # return wInput + wBiasInput + wHidden + wBiasHidden + wOutput + wBiasOutput

@jit(nopython=True)
def _mutate(DNA, mutationRate):
    mutations = math.floor(len(DNA) * mutationRate)
    for i in range(0, mutations):
        randId = random.randrange(0, len(DNA))
        DNA[randId] += random.gauss(0, 0.08)
    return DNA

@jit(nopython=True)
def _crossover(DNA1, DNA2):
    newDNA = DNA1
    for i in range(0, len(DNA1), 10):
        if random.random() < 0.5:
            newDNA[i:i + 10] = DNA2[i:i + 10]
    # assert len(newDNA) == len(DNA1), "New DNA constructed wrong"
    return newDNA


def toStr(DNA):
    dnaStr = "\n".join([str(elem) for elem in DNA], )
    return dnaStr

def fromStr(dnaStr):
    reader = csv.reader(dnaStr, delimiter='\n')
    DNA = []
    for row in reader:
        DNA.append(row[0][0])
    return DNA
