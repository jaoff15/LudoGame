import math
import random

from NeuralNetwork.Neuron import Neuron
import NeuralNetwork.ActivationFunctions as af
from NeuralNetwork.DNA import DNA


INPUT_NEURONS = 65
HIDDEN_NEURONS_PER_LAYER = 65
HIDDEN_LAYERS = 2
OUTPUT_NEURONS = 4


import config
from NeuralNetwork import DNA

# gBestIndividualDNA = None
# gSecondBestIndividualDNA = None

gLastPopulationResult = None
gPopulationWeights = []

def saveLastPolulation(LastPopulationResult): #bestIndividualDNA, secondBestIndividualDNA):
    # global gBestIndividualDNA
    # global gSecondBestIndividualDNA
    # gBestIndividualDNA = bestIndividualDNA
    # gSecondBestIndividualDNA = secondBestIndividualDNA

    global gLastPopulationResult
    gLastPopulationResult = LastPopulationResult

    global gPopulationWeights
    if gPopulationWeights == []:
        gPopulationWeights = list(range(0,len(LastPopulationResult)))


def _selectTwoIndividualsFromPopulation():
    global gLastPopulationResult
    individual1 = None
    individual2 = None
    dna = DNA.DNA()
    if gLastPopulationResult == None:
        # There is no population. Create two individuals.
        individual1 = dna.getDNA(NeuralNetwork(INPUT_NEURONS, HIDDEN_NEURONS_PER_LAYER, HIDDEN_LAYERS, OUTPUT_NEURONS))
        individual2 = dna.getDNA(NeuralNetwork(INPUT_NEURONS, HIDDEN_NEURONS_PER_LAYER, HIDDEN_LAYERS, OUTPUT_NEURONS))
    else:
        # Pick two individuals
        # Pick an individual with the probability of its index
        global gPopulationWeights
        n1 = random.choices(gPopulationWeights, gPopulationWeights)
        n2 = random.choices(gPopulationWeights, gPopulationWeights)
        individual1 = gLastPopulationResult[n1]["invididual"]
        individual2 = gLastPopulationResult[n2]["invididual"]

    return individual1, individual2


def createPopulation(populationSize):
    # global gBestIndividualDNA
    # global gSecondBestIndividualDNA
    # bestIndividualDNA = gBestIndividualDNA
    # secondBestIndividualDNA = gSecondBestIndividualDNA

    populationDNA = []
    dna = DNA.DNA()
    for i in range(0, populationSize):
        [dnaA, dnaB] = _selectTwoIndividualsFromPopulation()
        dnaC = dna.combineDNA(dnaA, dnaB)
        dnaC = dna.mutateDNA(dnaC)
        populationDNA.append(dnaC)
    return populationDNA

class NeuralNetwork:
    def __init__(self, noInput, noHidden, noHiddenLayers, noOutput,
                 inputWeights = None, inputBiasWeights = None,
                 hiddenWeights = None, hiddenBiasWeights = None,
                 outputWeights = None,outputBiasWeights = None):

        self.noInput = noInput
        self.input = []
        self.noHidden = noHidden
        self.noHiddenLayers = noHiddenLayers
        self.hidden = []
        self.noOutput = noOutput
        self.output = []

        self.inputWeights       = inputWeights
        self.inputBiasWeights   = inputBiasWeights
        self.hiddenWeights      = hiddenWeights
        self.hiddenBiasWeights  = hiddenBiasWeights
        self.outputWeights      = outputWeights
        self.outputBiasWeights  = outputBiasWeights



        self.initializeNN()


    def initializeNN(self):
        for i in range(0,self.noInput):
            w = None
            wb = None
            if self.inputWeights != None and self.inputBiasWeights != None:
                w = self.inputWeights
                wb = self.inputBiasWeights[i]

            # self.input.append(Neuron(af.NoActivationFunction(), self.noInput))
            self.input.append(Neuron(af.NoActivationFunction(), 1, w, wb))
        for i in range(0,self.noHiddenLayers):
            layer = []
            if i == 0:
                for j in range(0, self.noInput):
                    w = None
                    wb = None
                    if self.hiddenWeights != None and self.hiddenBiasWeights != None:
                        w  = self.hiddenWeights[:self.noInput]
                        wb = self.hiddenBiasWeights[j]
                    layer.append(Neuron(af.Logistic(), self.noInput, w, wb))
            else:
                for j in range(0, self.noHidden):
                    w = None
                    wb = None
                    if self.hiddenWeights != None and self.hiddenBiasWeights != None:
                        w  = self.hiddenWeights[self.noInput+(i-1)*self.noHidden:self.noInput+i*self.noHidden]
                        wb = self.hiddenBiasWeights[i*self.noHidden+j]
                    layer.append(Neuron(af.Logistic(), self.noHidden, w, wb))
            self.hidden.append(layer)

        for i in range(0,self.noOutput):
            w = None
            wb = None
            if self.outputWeights != None and self.outputBiasWeights != None:
                w = self.outputWeights
                wb = self.outputBiasWeights[i]
            self.output.append(Neuron(af.Logistic(), self.noHidden, w, wb))


    def ff(self, inputs):
        assert len(inputs) == self.noInput, "Input array has wrong size"

        inputLayer = []
        for i in range(0,self.noInput):
            # inputLayer.append(self.input[i].ff(inputs))
            inputLayer.append(self.input[i].ff([inputs[i]]))

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
            w.extend(n.weights)
        return w

    def getInputBiasWeights(self):
        w = []
        for n in self.input:
            w.append(n.bias)
        return w

    def getOutputWeights(self):
        w = []
        for n in self.output:
            w.extend(n.weights)
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
                w.extend(n.weights)
        return w

    def getHiddenBiasWeights(self):
        w = []
        for layer in range(0, self.noHiddenLayers):
            for n in self.hidden[layer]:
                w.append(n.bias)
        return w


