import math
import random
from numba import jit, cuda

from NeuralNetwork.Neuron import Neuron
import NeuralNetwork.ActivationFunctions as af
from NeuralNetwork.DNA import DNA


INPUT_NEURONS = 65
HIDDEN_NEURONS_PER_LAYER = 20 #*2+1
HIDDEN_LAYERS = 5
OUTPUT_NEURONS = 4

CARRY_OVER = 0

import config
from NeuralNetwork import DNA

gLastPopulationResult = None

def getBestIndividual():
    if gLastPopulationResult == None:
        return None
    else:
        return gLastPopulationResult[0][0]["DNA"]

def saveLastPolulation(LastPopulationResult):
    global gLastPopulationResult
    gLastPopulationResult = LastPopulationResult

def _getIndividualDnaI(i):
    global gLastPopulationResult
    if gLastPopulationResult == None:
        return None
    else:
        return gLastPopulationResult[i][0]["DNA"]

def _selectTwoIndividualsFromPopulation(lastPopulationFitnessList):
    # individual1 = None
    # individual2 = None
    dna = DNA.DNA()
    if len(lastPopulationFitnessList) == 0:
        # There is no population. Create two individuals.
        individual1 = dna.getDNA(NeuralNetwork(INPUT_NEURONS, HIDDEN_NEURONS_PER_LAYER, HIDDEN_LAYERS, OUTPUT_NEURONS))
        individual2 = dna.getDNA(NeuralNetwork(INPUT_NEURONS, HIDDEN_NEURONS_PER_LAYER, HIDDEN_LAYERS, OUTPUT_NEURONS))
    else:
        # n1 = 0
        # n2 = 1
        ids = list(range(0, len(gLastPopulationResult)))
        if config.ENABLE_CHECKS:
            assert len(ids) == len(lastPopulationFitnessList), "Index length and population fitness results length does not match"
        lids = len(ids)
        llastPopulationFitnessList = len(lastPopulationFitnessList)
        n1 = (random.choices(ids, lastPopulationFitnessList ,k=1))[0]
        n2 = (random.choices(ids, lastPopulationFitnessList ,k=1))[0]
        individual1 = gLastPopulationResult[n1][0]["DNA"]
        individual2 = gLastPopulationResult[n2][0]["DNA"]

    return individual1, individual2


def createPopulation(populationSize):
    populationDNA = []
    dna = DNA.DNA()
    # Carry over best individual from last generation
    for i in range(0, CARRY_OVER):
        dnaA = _getIndividualDnaI(i)
        if dnaA != None:
            populationDNA.append(dnaA)
    # Create new generation
    # Pick two individuals
    # Pick an individual with the probability of its index
    global gLastPopulationResult

    lastPopulationFitnessList = []
    if gLastPopulationResult != None:
        for i in range(0, len(gLastPopulationResult)):
            lastPopulationFitnessList.append(max(1,gLastPopulationResult[i][0]["fitness"]))
    if config.ENABLE_CHECKS:
        assert CARRY_OVER <= populationSize, "Carry over cannot be the same size or bigger than the population"
    for i in range(0, populationSize-CARRY_OVER):
        [dnaA, dnaB] = _selectTwoIndividualsFromPopulation(lastPopulationFitnessList)
        dnaC = dna.combineDNA(dnaA, dnaB)
        dnaC = dna.mutateDNA(dnaC)
        populationDNA.append(dnaC)
    return populationDNA

class NeuralNetwork:
    def __init__(self, noInput, noHidden, noHiddenLayers, noOutput,
                 inputWeights = None,  inputBiasWeights = None,
                 hiddenWeights = None, hiddenBiasWeights = None,
                 outputWeights = None, outputBiasWeights = None):

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
                w = [self.inputWeights[i]]
                wb = self.inputBiasWeights[i]

            # self.input.append(Neuron(af.NoActivationFunction(), self.noInput))
            self.input.append(Neuron(af.NoActivationFunction(), 1, w, wb))
        for i in range(0,self.noHiddenLayers):
            layer = []

            for j in range(0, self.noHidden):
                # Find weights for current neuron
                w = None
                wb = None
                if self.hiddenWeights != None and self.hiddenBiasWeights != None:
                    if i == 0:
                        w = self.hiddenWeights[:self.noInput]
                        wb = self.hiddenBiasWeights[j]
                    else:
                        w = self.hiddenWeights[self.noInput + (i - 1) * self.noHidden:self.noInput + i * self.noHidden]
                        wb = self.hiddenBiasWeights[i * self.noHidden + j]
                else:
                    # No weights present =>  initialise random neuron
                    pass
                # Append new neuron
                if i == 0:
                    layer.append(Neuron(af.Logistic(), self.noInput, w, wb))
                else:
                    layer.append(Neuron(af.Logistic(), self.noHidden, w, wb))

            self.hidden.append(layer)

        for i in range(0,self.noOutput):
            w = None
            wb = None
            if self.outputWeights != None and self.outputBiasWeights != None:
                w = self.outputWeights
                wb = self.outputBiasWeights[i]
            self.output.append(Neuron(af.Logistic(), self.noHidden, w, wb))

    @jit(target="cuda")
    def ff(self, inputs):
        if config.ENABLE_CHECKS:
            assert len(inputs) == self.noInput, "Input array has wrong size"

        inputLayer = []
        for i in range(0,self.noInput):
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

        # Create dice throw list
        diceNeurons = [0, 0, 0, 0, 0, 0]
        diceNeurons[dice-1] = 1


        # Process player data to make it easier to use later
        homeNeurons = [0]
        playerPiecePositions = []
        playerPieceFinishPositions = []
        for piece in player.pieces:
            if piece.atHome:
                homeNeurons[0] = 1
            elif (not piece.atHome and not piece.hasFinished) and not piece.onFinishStretch:
                playerPiecePositions.append(piece.pos)
            elif (not piece.atHome and not piece.hasFinished) and piece.onFinishStretch:
                playerPieceFinishPositions.append(piece.pos)

        # Create the board neurons
        boardNeurons = []
        for i in range(1,config.MAX_POSITIONS+1):
            if i in playerPiecePositions:
                boardNeurons.append(1)      # Position has a player piece
            elif board[i-1] == "Piece":
                boardNeurons.append(-1)     # Position has an enemy piece
            else:
                boardNeurons.append(0)      # Position is empty

        # Create the finishing straight neurons
        finishNeurons = [0, 0, 0, 0, 0, 0]
        for i in range(1,config.MAX_FINISH_LANE_POSITIONS+1):
            if i in playerPieceFinishPositions:
                finishNeurons[i-1] = 1

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

