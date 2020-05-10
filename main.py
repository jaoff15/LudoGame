
import Ludo
import matplotlib.pyplot as plt
from NeuralNetwork import NeuralNetwork as NN
import config


# This function performs a game of Ludo
def runGame(gameModes,gameId, popualationSize):

    ludo = Ludo.Ludo(gameModes)
    populationDNA =  NN.createPopulation(popualationSize)

    #bestIndividualDNA, secondBestIndividualDNA
    [bestFitness, populationResult] = ludo.play(gameId, populationDNA)
    NN.saveLastPolulation(populationResult) #bestIndividualDNA, secondBestIndividualDNA)

    ludo.reset()
        # winners.append(winner)
    return bestFitness
    # return (winners.count(3)/noGames)*100


if __name__ == '__main__':
    gameModes = ["NN", "RA", "RA", "RA"]

    cycles          = 100 # How many times should the ludo game be played
    fitnessResults  = [] # Array to hold result from the games
    winsLast100Games= 0
    gameId          = 1  # A way to lookup how many games has been performed
    populationSize  = 100 # How many individuals should the population contain

    for cycle in range(1, cycles + 1):
        print("Cycle: #%s" % (cycle))

        # Run game
        bestFitness = runGame(gameModes, gameId, populationSize)

        if config.PRINT_BEST_FITNESS_SCORE:
            print("Best Fitness: %s", (bestFitness))

        # Handle Analysis
        gameId += 1
        fitnessResults.append(bestFitness)

    x = list(range(0,len(fitnessResults)))
    plt.plot(x, fitnessResults)

    plt.xlabel('Games')
    plt.ylabel('Fitness score')
    plt.show()