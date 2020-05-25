import math
import numpy as np
import random

class Population:
    def __init__(self, populationSize, geneCount):
        self.populationSize = populationSize
        self.geneCount      = geneCount
        self.pieceCount     = 4
        self.elitismCount   = 10
        self.mutationRate   = 0.10
        # self.mutationRate   = 0.02
        self.lastPopulation = np.zeros((self.populationSize, self.geneCount*self.pieceCount))
        self.lastPopulationFitness = []

    def saveLastPopulation(self, lastPopulationFitness,lastPopulation):
        self.lastPopulation        = lastPopulation
        self.lastPopulationFitness = lastPopulationFitness

    def createPopulation(self,gameId):
        population = np.zeros((self.populationSize, self.geneCount*self.pieceCount))

        for i in range(0, self.populationSize):
            if gameId == 1:
                # first generation
                population[i] = np.random.rand(self.geneCount*self.pieceCount)
            else:
                if i < self.elitismCount:
                    # Do elitism
                    population[i] = self.lastPopulation[i]
                if i > self.elitismCount:
                    # Do crossover and mutation
                    # Pick 2 individuals
                    ids = np.arange(self.populationSize)
                    #   Make difference between good and bad bigger
                    fitnessListScaled = self.lastPopulationFitness * np.logspace(2, 0, len(self.lastPopulationFitness))
                    #   Shift up
                    fitnessList = fitnessListScaled + 1
                    #   Choose two individuals
                    [n1, n2] = (random.choices(ids, fitnessList, k=2))
                    if n1 == n2: n2 += 1    # Make sure its not the same individual chosen twice
                    if n2 >= self.populationSize: n2 = n1-1
                    individual1 = self.lastPopulation[n1]
                    individual2 = self.lastPopulation[n2]

                    # Crossover
                    newIndividual = self._crossover(individual1, individual2)
                    # Mutation
                    newIndividual = self._mutation(newIndividual)

                    # Insert into population
                    population[i] = newIndividual
        # self.lastPopulation = population
        return population, self.populationSize

    def _crossover(self, individual1, individual2):
        assert len(individual1) == len(individual2), "The parents should have the same length"
        newIndividual = individual1
        for i in range(0, len(newIndividual)):
            if random.random() > 0.5:
                newIndividual[i] = individual2[i]
        assert len(newIndividual) == len(individual1), "New individual has wrong length"
        return newIndividual

    def _mutation(self, individual):
        # randomly select an amount of mutations depending on the mutation rate
        while random.random() < self.mutationRate:
            # Choose the weight to modify
            index = random.randint(0, len(individual)-1)
            # Modify weight by random amount
            # individual[index] += random.gauss(0, 0.15)
            individual[index] += random.gauss(0, 0.4)
        return individual