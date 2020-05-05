
from NeuralNetwork.Neuron import Neuron
import NeuralNetwork.ActivationFunctions as af

import config
from NeuralNetwork import DNA

def createPopulation(populationSize, bestIndividual, secondBestIndividual):
    dna = DNA.DNA()
    dnaA = dna.getDNA(bestIndividual.NN)
    dnaB = dna.getDNA(secondBestIndividual.NN)
    population = []
    for i in range(0, populationSize):
        dnaC = dna.combineDNA(dnaA, dnaB)
        dnaC = dna.mutateDNA(dnaC)
        populationDNA.append(dnaC)
    return populationDNA

class NeuralNetwork:
    def __init__(self, noInput, noHidden, noHiddenLayers, noOutput,
                 inputWeights = None, inputBiasWeights = None,
                 hiddenWeights = None, hiddenBiasWeights = None,
                 outputWeights = None,outputBiasWeights = None):

        self.mutationRate = 0.001

        self.inputWeights       = inputWeights
        self.inputBiasWeights   = inputBiasWeights
        self.hiddenWeights      = hiddenWeights
        self.hiddenBiasWeights  = hiddenBiasWeights
        self.outputWeights      = outputWeights
        self.outputBiasWeights  = outputBiasWeights

        self.noInput    = noInput
        self.input      = []
        self.noHidden   = noHidden
        self.noHiddenLayers = noHiddenLayers
        self.hidden     = []
        self.noOutput   = noOutput
        self.output     = []

        self.initializeNN()


    def initializeNN(self):
        for i in range(0,self.noInput):
            w = None
            if self.inputWeights != None:
                w = self.inputWeights[i]

            # self.input.append(Neuron(af.NoActivationFunction(), self.noInput))
            self.input.append(Neuron(af.NoActivationFunction(), 1, w))
        for i in range(0,self.noHiddenLayers):
            layer = []
            for j in range(0, self.noHidden):
                if i == 0:
                    layer.append(Neuron(af.Logistic(), self.noInput))
                else:
                    layer.append(Neuron(af.Logistic(), self.noHidden))
            self.hidden.append(layer)

        for i in range(0,self.noOutput):
            self.output.append(Neuron(af.Logistic(), self.noHidden))


    def ff(self, inputs):
        assert len(inputs) == self.noInput, "Input array has wrong size"

        inputLayer = []
        for i in range(0,self.noInput):
            # inputLayer.append(self.input[i].ff(inputs))
            inputLayer.append(self.input[i].ff(inputs(i)))

        hiddenLayerLast = []
        for i in range(0,self.noHiddenLayers):
            hiddenLayer = []
            for j in range(0, self.noHidden):
                if i == 0:
                    hiddenLayer.append(self.hidden[i][j].ff(inputLayer))
                else:
                    hiddenLayer.append(self.hidden[i][j].ff(hiddenLayerLast))
            hiddenLayerLast = hiddenLayer

        outputLayer = []
        for i in range(0,self.noOutput):
            outputLayer.append(self.output[i].ff(hiddenLayerLast))

        return outputLayer

    def constructNNInput(self, board, dice, player, players):
        diceNeurons = []
        boardNeurons = []
        finishNeurons = []
        homeNeurons = [0]

        for i in range(1,6+1):
            if i == dice:
                diceNeurons.append(1)
            else:
                diceNeurons.append(0)

        playerPiecePositions = []
        playerPieceFinishPositions = []
        for piece in player.pieces:
            if (not piece.atHome or piece.hasFinished) and not piece.onFinishStretch:
                playerPiecePositions.append(piece.pos+1)
            elif (not piece.atHome or piece.hasFinished) and piece.onFinishStretch:
                playerPieceFinishPositions.append(piece.pos + 1)
            if piece.atHome:
                homeNeurons[0] = 1
        for i in range(1,52+1):
            if i in playerPiecePositions:
                boardNeurons.append(1)      # Position has a player piece
            elif board[i-1] == "Piece":
                boardNeurons.append(-1)  # Position has an enemy piece
            else:
                boardNeurons.append(0)  # Position is empty

        for i in range(1,6+1):
            if i in playerPieceFinishPositions:
                finishNeurons.append(1)
            else:
                finishNeurons.append(0)

        return diceNeurons + boardNeurons + finishNeurons + homeNeurons

    def getInputWeights(self):
        w = []
        for n in self.input:
            w.append(n.weights)
        return w

    def getInputBiasWeights(self):
        w = []
        for n in self.input:
            w.append(n.bias)
        return w

    def getOutputWeights(self):
        w = []
        for n in self.output:
            w.append(n.weights)
        return w

    def getOutputBiasWeights(self):
        w = []
        for n in self.output:
            w.append(n.bias)
        return w

    def getHiddenWeights(self):
        w = []
        for layer in range(0,self.noHiddenLayers):
            for n in self.hidden[layer]:
                w.append(n.weights)
        return w

    def getHiddenBiasWeights(self):
        w = []
        for layer in range(0, self.noHiddenLayers):
            for n in self.hidden[layer]:
                w.append(n.bias)
        return w


