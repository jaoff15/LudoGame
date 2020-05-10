
import random
import math
import NeuralNetwork as NN

class DNA:
    def __init__(self):
        self.mutationRate = 0.005

    def extractFromDNA(self, DNA, noInput, noHidden, noHiddenLayers, noOutput):
        requestedLength  = noInput + noInput         # Input Layer
        requestedLength += noInput*noHidden+(noHidden)   # First hidden layer
        requestedLength += (noHiddenLayers-1) * noHidden*noHidden+(noHidden) # Rest of the hidden layers
        requestedLength += noOutput*noHidden+(noOutput)  # Output Layer
        assert requestedLength == len(DNA), "DNA and requested lengths are not equal"
        #wInput, wBiasInput, wHidden, wBiasHidden, wOutput, wBiasOutput = []
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
            # [nxtIndex, nxtIndex+noHidden] = Hidden Weights
            wHidden.extend(DNA[nxtIndex:nxtIndex + noHidden*noHidden])
            nxtIndex += noHidden*noHidden

            # [nxtIndex,nxtIndex+1] = Hidden Bias Weights
            wBiasHidden.extend(DNA[nxtIndex:nxtIndex + noHidden])
            nxtIndex += noHidden

        # [nxtIndex, nxtIndex+noOutput] = Output Weights
        wOutput = DNA[nxtIndex:nxtIndex + noHidden*noOutput]
        nxtIndex += noHidden*noOutput

        wBiasOutput = DNA[nxtIndex:nxtIndex + noOutput]
        nxtIndex += noOutput

        buildLength = len(wInput) + len(wBiasInput)  + len(wOutput) + len(wBiasOutput)+ len(wHidden) + len(wBiasHidden)

        # for h in range(0, noHiddenLayers):
        #     buildLength += len(wHidden[h][:]) + len(wBiasHidden[h][:])
       # assert buildLength == len(DNA), "DNA and build lengths are not equal"

        return wInput, wBiasInput, wHidden, wBiasHidden, wOutput, wBiasOutput

    def mutateDNA(self, DNA):
        mutations = math.floor(len(DNA) * self.mutationRate)
        for i in range(0, mutations):
            randId = random.randrange(0,len(DNA))
            DNA[randId] = random.random()
        return DNA

    def combineDNA(self, DNA1, DNA2):
        newDNA = []
        lastI = 0
        for i in range(0, len(DNA1), 10):
            if random.random() < 0.5:
                newDNA.extend(DNA1[i:i+10])
            else:
                newDNA.extend(DNA2[i:i+10])
            lastI = i
        # if random.random() < 0.5:
        #     newDNA.extend(DNA1[lastI:])
        # else:
        #     newDNA.extend(DNA2[lastI:])
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
