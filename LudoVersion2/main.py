import time
import numpy as np
import cProfile

import Ludo
import Dice

# from Ludo64bitVersion.NeuralNetwork import NeuralNetwork as NN
import config
import FileHandling as FH
from NeuralNetwork import DNA

import Population

gFitnessFileName = "fitness.csv"
gRandFitnessFileName = "random_fitness.csv"
gTiesFileName = "ties.csv"
gWeightFileName = "weights.csv"
# def game(gameModes, gameId, pop, geneCount, turns, gamesPerGeneration):
#     # Get a Ludo game
#     ludo = Ludo.Ludo(gameModes)
#     return ludo.play(gameId, pop, geneCount,turns, gamesPerGeneration)



# This function performs a game of Ludo
def runGame(gameModes,gameId, population, geneCount, turns, gamesPerGeneration):
    if config.PRINT_EXECUTION_TIME:
        # Start generation timer
        start = time.time()


    # Create a new generation
    [pop,populationSize] = population.createPopulation(gameId)

    # # Create the dicethrows offered to the Neural Network for the games
    # diceThrows = Dice.generateDiceThrows(turns)


    # Play the Ludo game with the current population
    ludo = Ludo.Ludo(gameModes)
    [populationResult, randomResult, ties] = ludo.play(gameId, pop, geneCount, turns, gamesPerGeneration)

    # Extract fitness values from population
    populationFitness = np.zeros(populationSize)
    for i in range(0, populationSize):
        populationFitness[i] = populationResult[i][0]["fitness"]

    # Extract genes from population
    lastPopulation = np.zeros((populationSize, geneCount*4))
    for i in range(0, populationSize):
        lastPopulation[i] = populationResult[i][0]["DNA"]

    # Find max, avg, min fitnesses from population
    playerFitnessData = {"max": np.max(populationFitness), "avg": np.average(populationFitness),
                         "min": np.min(populationFitness)}

    randomFitnessData = {"max": np.max(randomResult), "avg": np.average(randomResult),
                         "min": np.min(randomResult)}

    # Save the fitness results from the ludo game
    population.saveLastPopulation(populationFitness,lastPopulation)

    if config.PRINT_EXECUTION_TIME:
        # Stop and show generation time
        end = time.time()
        print("Generation Time: %s ms" % ((end - start) * 1000.00))

    # return bestFitness, winners, avgGenerationFitness, totalRandomPlayerData
    return playerFitnessData,randomFitnessData, ties, lastPopulation[0]


def main():
    # Log Time
    start = time.time()

    # Create files
    fitnessFile = FH.makeNewFile(gFitnessFileName)
    randomFile = FH.makeNewFile(gRandFitnessFileName)
    tieFile = FH.makeNewFile(gTiesFileName)
    weightfile = FH.makeNewFile(gWeightFileName)

    gameModes = ["AI", "RA", "RA", "RA"]

    generations         = 100 # How many times should the ludo game be played
    gamesPerGeneration  = 100
    gameId              = 1  # A way to lookup how many games has been performed
    populationSize      = 100  # How many individuals should the population contain
    geneCount           = 8 #28
    turns               = 300

    population = Population.Population(populationSize,geneCount)

    for generation in range(1, generations + 1):
        print("\nGeneration: #%s" % (generation))

        # Run game
        [playerFitnessData,randomFitnessData, ties, bestIndividual] = runGame(gameModes, generation, population, geneCount, turns, gamesPerGeneration)


        # Save fitness results
        FH.appendToFile(fitnessFile, (str(generation) + ',' + str(playerFitnessData['max'])+',' + str(playerFitnessData['avg'])+',' + str(playerFitnessData['min'])))
        FH.appendToFile(randomFile, (str(generation) + ',' + str(randomFitnessData['max']) + ',' + str(randomFitnessData['avg']) + ',' + str(randomFitnessData['min'])))
        FH.writeToFile(weightfile, str(bestIndividual))
        FH.appendToFile(tieFile, (str(generation) + str(ties)))

    # Time measurement
    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Executing Time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))


if __name__ == '__main__':
    # cProfile.run("main()")
    main()