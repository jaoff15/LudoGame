import time
import cProfile
import math
import multiprocessing, time, signal


import Ludo
import Dice

from NeuralNetwork import NeuralNetwork as NN
import config
import FileHandling as FH
from NeuralNetwork import DNA

gWeightsFileName = "weights.csv"
gFitnessFileName = "fitness.csv"
gAvgGenFitnessFileName = "avg_gen_fitness.csv"
gWinPercentFileName = "win_percent.csv"
gWinnersFileName = "winners.csv"


gMAX_FITNESS = 1000
def testPerformance(noGames, gameModes, gameId, individual):

    noWins = 0
    for i in range(0, noGames):
        # Get a Ludo game
        ludo = Ludo.Ludo(gameModes)

        # Play the Ludo game with individual
        maxRounds = 1000
        diceThrows = Dice.generateDiceThrows(maxRounds)
        [fitness, result, winners, avgGenerationFitness] = ludo.play(gameId, [individual], diceThrows, maxRounds)
        global gMAX_FITNESS
        if fitness >= gMAX_FITNESS:
            noWins += 1

    winPercent = (noWins/noGames) * 100.00
    return winPercent


def game(gameModes, gameId, populationDNA, diceThrows, maxRounds):
    # Get a Ludo game
    ludo = Ludo.Ludo(gameModes)

    return ludo.play(gameId, populationDNA,diceThrows,maxRounds)

# def dividePopulationInto4(pop, popSize):
#     c1 = pop[:math.floor(popSize/4)]
#     c2 = pop[math.floor(popSize / 4):math.floor(popSize / 2)]
#     c3 = pop[math.floor(popSize / 2):math.floor(3 * popSize / 4)]
#     c4 = pop[math.floor(3 * popSize / 4):]
#     return [c1, c2, c3, c4]

# This function performs a game of Ludo
def runGame(gameModes,gameId, popualationSize):
    if config.PRINT_EXECUTION_TIME:
        # Start generation timer
        start = time.time()

    # Create a new generation
    populationDNA =  NN.createPopulation(popualationSize)

    # Calculate the number of rounds that the Ludo game should run for
    maxRounds = min(160, math.ceil(gameId / 160.0) * 20)
    # maxRounds = 1000

    # Create the dicethrows offered to the Neural Network for the games
    diceThrows = Dice.generateDiceThrows(maxRounds)


    # Play the Ludo game with the current population
    [bestFitness, populationResult, winners,avgGenerationFitness] = game(gameModes, gameId, populationDNA, diceThrows, maxRounds)

    # Save the fitness results from the ludo game
    NN.saveLastPolulation(populationResult)

    if config.PRINT_EXECUTION_TIME:
        # Stop and show generation time
        end = time.time()
        print("Generation Time: %s ms" % ((end - start) * 1000.00))

    return bestFitness, winners, avgGenerationFitness


# TODO Improve performance
# TODO Save average generation fitness



def main():
    # Log Time
    start = time.time()

    # Create files
    weightsFile = FH.makeNewFile(gWeightsFileName)
    fitnessFile = FH.makeNewFile(gFitnessFileName)
    winPercentFile = FH.makeNewFile(gWinPercentFileName)
    winnersFile = FH.makeNewFile(gWinnersFileName)
    avgGenFitness = FH.makeNewFile(gAvgGenFitnessFileName)


    gameModes = ["NN", "RA", "RA", "RA"]

    cycles          = 10000 # How many times should the ludo game be played
    gameId          = 1  # A way to lookup how many games has been performed
    populationSize  = 100  # How many individuals should the population contain


    winPercent          = []
    cyclesBetweenTests  = 100
    testCycles          = 100

    for cycle in range(1, cycles + 1):
        # Run game
        [bestFitness, winners,avgGenerationFitness] = runGame(gameModes, gameId, populationSize)

        print("\nGeneration: #%s" % (cycle))

        # Save fitness results
        FH.appendToFile(fitnessFile, (str(gameId) + ',' + str(bestFitness)))
        FH.appendToFile(avgGenFitness, (str(gameId) +','+ str(avgGenerationFitness)))
        if config.PRINT_BEST_FITNESS_SCORE:
            print("Best Fitness: %s" % (bestFitness))

        if gameId > 1:
            FH.appendListToFile(winnersFile, str(gameId), winners)

        # Handle Analysis
        gameId += 1

        # Get best individual
        bestIndividual = NN.getBestIndividual()

        # Write best individual to file
        FH.writeToFile(weightsFile, DNA.toStr(bestIndividual))

        # Once in a while make a performance test of the last best individual
        if cycle % cyclesBetweenTests == 0:
            # Perform tests
            if len(bestIndividual) != 0:
                winPercent.append(testPerformance(testCycles, gameModes, gameId, bestIndividual))
                print("Win percent %s" % (winPercent[-1]))
                # Write result to file
                FH.appendToFile(winPercentFile, (str(gameId) + ',' + str(winPercent[-1])))


    # Time measurement
    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Executing Time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))


if __name__ == '__main__':
    # cProfile.run("main()")
    main()