import math
import random
import numpy as np


from Ludo64bitVersion.NeuralNetwork import Neuron
from Ludo64bitVersion.NeuralNetwork import ActivationFunctions as af
from Ludo64bitVersion import config
from Ludo64bitVersion.NeuralNetwork import DNA

# INPUT_NEURONS = 60
# INPUT_NEURONS = 65
# INPUT_NEURONS = 60*4
INPUT_NEURONS = 60*2
# HIDDEN_NEURONS_PER_LAYER = INPUT_NEURONS*2+1
HIDDEN_NEURONS_PER_LAYER = INPUT_NEURONS+1
HIDDEN_LAYERS = 1
OUTPUT_NEURONS = 1

CARRY_OVER = 10



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
        return []
    else:
        return gLastPopulationResult[i][0]["DNA"]

def _selectTwoIndividualsFromPopulation(lastPopulationFitnessList,gLastPopulationResult):
    dna = DNA.DNA()
    if gLastPopulationResult == None:
        # There is no population. Create two individuals.
        individual1 = dna.getDNA(NeuralNetwork(INPUT_NEURONS, HIDDEN_NEURONS_PER_LAYER, HIDDEN_LAYERS, OUTPUT_NEURONS))
        individual2 = dna.getDNA(NeuralNetwork(INPUT_NEURONS, HIDDEN_NEURONS_PER_LAYER, HIDDEN_LAYERS, OUTPUT_NEURONS))
    else:
        # ids = list(range(0, len(gLastPopulationResult)))
        ids = np.arange(len(gLastPopulationResult))
        if config.ENABLE_CHECKS:
            assert len(ids) == len(lastPopulationFitnessList), "Index length and population fitness results length does not match"
        # first scale population fitness up to make the better individuals stand out more
        fitnessListScaled = lastPopulationFitnessList*np.logspace(2,0,len(lastPopulationFitnessList))
        # Make fitness list start at 1
        fitnessList = fitnessListScaled - np.min(fitnessListScaled) + 1
        [n1,n2] = (random.choices(ids, fitnessList ,k=2))
        if n1 == n2: n2 += 1
        individual1 = gLastPopulationResult[n1][0]["DNA"]
        individual2 = gLastPopulationResult[n2][0]["DNA"]

    return individual1, individual2


def createPopulation(populationSize):
    return createPopulation_1(populationSize)
    # return createPopulation_2(populationSize)

def createPopulation_1(populationSize):
    # 10% elitism
    # 90% crossover + mutation
    dna = DNA.DNA()
    populationDNA = np.zeros((populationSize, DNA.expectedDnaLength(INPUT_NEURONS,HIDDEN_NEURONS_PER_LAYER,HIDDEN_LAYERS,OUTPUT_NEURONS)))
    # Carry over best individual from last generation
    for i in range(0, CARRY_OVER):
        dnaA = _getIndividualDnaI(i)
        if len(dnaA) != 0:
            populationDNA[i] = dnaA
    # Create new generation
    # Pick two individuals
    # Pick an individual with the probability of its index
    global gLastPopulationResult

    # lastPopulationFitnessList = []
    lastPopulationFitnessList = np.zeros(populationSize)
    if gLastPopulationResult != None:
        for i in range(0, len(gLastPopulationResult)):
            # lastPopulationFitnessList[i] = (max(1, gLastPopulationResult[i][0]["fitness"]))
            lastPopulationFitnessList[i] = gLastPopulationResult[i][0]["fitness"]
    if config.ENABLE_CHECKS:
        assert CARRY_OVER <= populationSize, "Carry over cannot be the same size or bigger than the population"
        assert CARRY_OVER != 0, "Carry over should not be 0 for a system with elitism."
    for i in range(0, populationSize-CARRY_OVER):
        [dnaA, dnaB] = _selectTwoIndividualsFromPopulation(lastPopulationFitnessList,gLastPopulationResult)
        dnaC = dna.combineDNA(dnaA, dnaB)
        dnaC = dna.mutateDNA(dnaC)
        populationDNA[i] = (dnaC)
    return populationDNA

def createPopulation_2(populationSize):
    # 10% elitism
    # 10% elitism + mutation
    # 10% random
    # 70% crossover + mutation
    dna = DNA.DNA()
    populationDNA = np.zeros((populationSize, DNA.expectedDnaLength(INPUT_NEURONS,HIDDEN_NEURONS_PER_LAYER,HIDDEN_LAYERS,OUTPUT_NEURONS)))
    currentPopulatonSize = 0
    # Elitism
    for i in range(0, math.floor(populationSize/10)):
        dnaA = _getIndividualDnaI(i)
        if len(dnaA) != 0:
            populationDNA[i] = dnaA
            currentPopulatonSize +=1
    # Elitism + mutation
    for i in range(0, math.floor(populationSize/10)):
        dnaA = _getIndividualDnaI(i)
        if len(dnaA) != 0:
            dnaA = dna.mutateDNA(dnaA)
            populationDNA[i] = dnaA
            currentPopulatonSize += 1
    # Random
    for i in range(0, math.floor(populationSize/10)):
        populationDNA[i] = dna.getDNA(NeuralNetwork(INPUT_NEURONS, HIDDEN_NEURONS_PER_LAYER, HIDDEN_LAYERS, OUTPUT_NEURONS))
        currentPopulatonSize += 1

    # Crossover and mutation
    global gLastPopulationResult
    lastPopulationFitnessList = np.zeros(populationSize)
    if gLastPopulationResult != None:
        for i in range(0, len(gLastPopulationResult)):
            lastPopulationFitnessList[i] = (max(1, gLastPopulationResult[i][0]["fitness"]))
    for i in range(0, populationSize-currentPopulatonSize):
        [dnaA, dnaB] = _selectTwoIndividualsFromPopulation(lastPopulationFitnessList,gLastPopulationResult)
        dnaC = dna.combineDNA(dnaA, dnaB)
        dnaC = dna.mutateDNA(dnaC)
        populationDNA[i] = (dnaC)
    return populationDNA



class NeuralNetwork:
    def __init__(self, noInput, noHidden, noHiddenLayers, noOutput,
                 inputWeights  = [], inputBiasWeights  = [],
                 hiddenWeights = [], hiddenBiasWeights = [],
                 outputWeights = [], outputBiasWeights = []):

        self.noInput        = noInput
        self.input          = [None] * self.noInput
        self.noHidden       = noHidden
        self.noHiddenLayers = noHiddenLayers
        self.hidden         = [None] * self.noHiddenLayers
        self.noOutput       = noOutput
        self.output         = [None] * self.noOutput


        self.inputWeights       = inputWeights
        self.inputBiasWeights   = inputBiasWeights
        self.hiddenWeights      = hiddenWeights
        self.hiddenBiasWeights  = hiddenBiasWeights
        self.outputWeights      = outputWeights
        self.outputBiasWeights  = outputBiasWeights


        self.initializeNN()


    def initializeNN(self):
        for i in range(0,self.noInput):
            w = []
            wb = []
            if len(self.inputWeights) != 0 and len(self.inputBiasWeights) != 0:
                w = [self.inputWeights[i]]
                wb = self.inputBiasWeights[i]
            self.input[i] = (Neuron.Neuron(af.NoActivationFunction(), 1, w, wb))
        for i in range(0,self.noHiddenLayers):
            layer = [None] * self.noHidden

            for j in range(0, self.noHidden):
                # Find weights for current neuron
                w = []
                wb = []
                if len(self.hiddenWeights) != 0 and len(self.hiddenBiasWeights) != 0:
                    if i == 0:
                        w = self.hiddenWeights[:self.noInput]
                    else:
                        start = self.noInput + (i - 1) * self.noHidden
                        end = self.noInput + i * self.noHidden
                        w = self.hiddenWeights[start:end]
                    wb = self.hiddenBiasWeights[i * self.noHidden + j]
                else:
                    # No weights present =>  initialise random neuron
                    pass
                # Add new neuron
                if i == 0:
                    layer[j] = (Neuron.Neuron(af.Logistic(), self.noInput, w, wb))
                else:
                    layer[j] =(Neuron.Neuron(af.Logistic(), self.noHidden, w, wb))

            self.hidden[i] = layer

        for i in range(0,self.noOutput):
            w = []
            wb = []
            if len(self.outputWeights) != 0 and len(self.outputBiasWeights) != 0:
                w = self.outputWeights[i*self.noHidden:(i+1)*self.noHidden]
                wb = self.outputBiasWeights[i]
            self.output[i] = (Neuron.Neuron(af.Logistic(), self.noHidden, w, wb))


    def ff(self, inputs):
        if config.ENABLE_CHECKS:
            assert len(inputs) == self.noInput, "Input array has wrong size"

        inputLayer = np.zeros(self.noInput)
        for i in range(0,self.noInput):
            inputLayer[i] = self.input[i].ff([np.array(inputs[i])])


        # First hidden layer
        hiddenLayer = np.zeros(self.noHidden)
        for j in range(0, self.noHidden):
            hiddenLayer[j] = self.hidden[0][j].ff(inputLayer)
        hiddenLayerLast = hiddenLayer

        # Rest of the hidden layers
        for i in range(1,self.noHiddenLayers):
            hiddenLayer = np.zeros(self.noHidden)
            for j in range(0, self.noHidden):
                hiddenLayer[j] = self.hidden[i][j].ff(hiddenLayerLast)
            hiddenLayerLast = hiddenLayer

        outputLayer = np.zeros(self.noOutput)
        for i in range(0,self.noOutput):
            outputLayer[i] = self.output[i].ff(hiddenLayerLast)

        return outputLayer


    # def constructNNInput(self, board, dice, player):
    #     # Create dice throw list
    #     diceNeurons = np.zeros(6)
    #     diceNeurons[math.floor(dice)-1] = 1.0
    #     # diceNeurons = np.zeros(1)
    #     # diceNeurons[0] = ([0.0,0.2,0.4,0.6,0.8,1.0])[math.floor(dice)-1]
    #
    #     # Process player data to make it easier to use later
    #     homeNeurons = np.zeros(1)
    #     boardNeurons = np.zeros(config.MAX_POSITIONS)
    #     finishNeurons = np.zeros(6)
    #
    #     # Version 2
    #     for piece in player.pieces:
    #         if piece.atHome:
    #             homeNeurons[0] = 1.0
    #         elif not piece.hasFinished:
    #             if piece.onFinishStretch:
    #                 # finishNeurons[math.floor(piece.pos)] = ([0.2,0.4,0.6,0.8])[piece.id-1]
    #                 finishNeurons[math.floor(piece.pos)] = 1.0
    #             else:
    #                 # boardNeurons[math.floor(piece.pos) - 1] = ([0.2, 0.4, 0.6, 0.8])[piece.id - 1]
    #                 boardNeurons[math.floor(piece.pos) - 1] = 1.0
    #
    #     for i in range(0,len(board)):
    #         if board[i] == 1 and boardNeurons[i] == 0:
    #             boardNeurons[i] = -1.0
    #
    #     return np.array(np.concatenate((diceNeurons, boardNeurons, finishNeurons, homeNeurons)))


    def getInputWeights(self):
        w = np.zeros(self.noInput)
        for i in range(0, self.noInput):
            n = self.input[i]
            w[i] = n.weights
        return w.flatten()

    def getInputBiasWeights(self):
        w = np.zeros(self.noInput)
        for i in range(0, self.noInput):
            n = self.input[i]
            if len(n.bias) > 0:
                w[i] = n.bias[0]
        return w

    def getOutputWeights(self):
        w = np.zeros((self.noOutput, self.noHidden))
        for i in range(0, self.noOutput):
            n = self.output[i]
            w[i] = n.weights
        return w.flatten()

    def getOutputBiasWeights(self):
        w = np.zeros(self.noOutput)
        for i in range(0, self.noOutput):
            n = self.output[i]
            if len(n.bias) > 0:
                w[i] = n.bias[0]
        return w

    def getHiddenWeights(self):
        w0 = np.zeros((self.noHidden,self.noInput))
        w1 = np.zeros((self.noHidden*(self.noHiddenLayers-1),self.noHidden))

        # First hidden layer
        for i in range(0, self.noHidden):
            n = self.hidden[0][i]
            w0[i] = n.weights

        nxtI = 0
        for i in range(1,self.noHiddenLayers):
            for j in range(0,self.noHidden):
                n = self.hidden[i][j]
                w1[nxtI] = n.weights
                nxtI += 1
        w0 = w0.flatten()
        w1 = w1.flatten()
        return np.concatenate((w0,w1))

    def getHiddenBiasWeights(self):
        w = np.zeros(self.noHiddenLayers*self.noHidden)
        for layer in range(0, self.noHiddenLayers):
            for i in range(0, self.noHidden):
                n = self.hidden[layer][i]
                if len(n.bias) > 0:
                    w[i] = n.bias[0]
        return w

