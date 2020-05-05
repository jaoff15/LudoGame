
import random
import NeuralNetwork as NN

class DNA:
    def __init__(self):
        pass

    def extractFromDNA(self, DNA, noInput, noHidden, noHiddenLayers, noOutput):
        requestedLength  = noInput * 2          # Input Layer
        requestedLength += noInput*2*noHidden   # First hidden layer
        requestedLength += (noHiddenLayers-1) * 2*noHidden*noHidden # Rest of the hidden layers
        requestedLength += 2*noOutput*noHidden  # Output Layer
        assert requestedLength == len(DNA), "DNA and requested lengths are not equal"
        #wInput, wBiasInput, wHidden, wBiasHidden, wOutput, wBiasOutput = []
        nxtIndex = 0

        # [nxtIndex, nxtIndex+noInput]          = Input Weights
        wInput = DNA[nxtIndex:nxtIndex+noInput]
        nxtIndex += noInput

        # [nxtIndex,nxtIndex+1] = Input Bias Weights
        wBiasInput = DNA[nxtIndex:nxtIndex + noInput]
        nxtIndex +=noInput

        wHidden = []
        wBiasHidden = []
        for h in range(0,noHiddenLayers):
            # [nxtIndex, nxtIndex+noHidden] = Hidden Weights
            wHidden.append(DNA[nxtIndex:nxtIndex + noHidden])
            nxtIndex += noHidden

            # [nxtIndex,nxtIndex+1] = Hidden Bias Weights
            wBiasHidden.append(DNA[nxtIndex:nxtIndex + noHidden])
            nxtIndex += noHidden

        # [nxtIndex, nxtIndex+noOutput] = Output Weights
        wOutput = DNA[nxtIndex:nxtIndex + noOutput]
        nxtIndex += noOutput

        wBiasOutput = DNA[nxtIndex:nxtIndex + noOutput]
        nxtIndex += noOutput

        buildLength = len(wInput) + len(wBiasInput)  + len(wOutput) + len(wBiasOutput)
        for h in range(0, noHiddenLayers):
            buildLength += len(wHidden[h][:]) + len(wBiasHidden[h][:])
        assert buildLength == len(DNA), "DNA and build lengths are not equal"

        return wInput, wBiasInput, wHidden, wBiasHidden, wOutput, wBiasOutput

    def mutateDNA(self, DNA):
        for i in range(0, len(DNA)):
            if random.random() < self.mutationRate:
                DNA[i] = random.random()

    def combineDNA(self, DNA1, DNA2):
        newDNA = []
        for i in range(0, len(DNA1)):
            if i < 0.5:
                newDNA.append(DNA1[i])
            else:
                newDNA.append(DNA2[i])

    def getDNA(self, NN):
        wInput      = NN.getInputWeights()
        wBiasInput  = NN.getInputBiasWeights()
        wHidden     = NN.getHiddenWeights()
        wBiasHidden = NN.getHiddenBiasWeights()
        wOutput     = NN.getOutputWeights()
        wBiasOutput = NN.getOutputBiasWeights()
        return wInput + wBiasInput + wHidden + wBiasHidden + wOutput + wBiasOutput
