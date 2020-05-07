
import Ludo
import matplotlib.pyplot as plt
from NeuralNetwork import NeuralNetwork as NN

# This function performs a game of Ludo
def runNGames(gameModes,gameId, popualationSize):

    ludo = Ludo.Ludo(gameModes)
    populationDNA =  NN.createPopulation(popualationSize)

    [bestFitness, bestIndividualDNA, secondBestIndividualDNA] = ludo.play(gameId, populationDNA)
    NN.saveLastPolulation(bestIndividualDNA, secondBestIndividualDNA)

    ludo.reset()
        # winners.append(winner)
    return bestFitness
    # return (winners.count(3)/noGames)*100


if __name__ == '__main__':
    gameModes = ["NN", "RA", "RA", "RA"]

    cycles          = 10 # How many times should the ludo game be played
    fitnessResults  = [] # Array to hold result from the games
    winsLast100Games= 0
    gameId          = 1  # A way to lookup how many games has been performed
    populationSize  = 10 # How many individuals should the population contain

    for cycle in range(1, cycles + 1):
        print("Cycle: #%s" % (cycle))

        # Run game
        bestFitness = runNGames(gameModes, gameId, populationSize)

        # Handle Analysis
        gameId += 1
        fitnessResults.append(bestFitness)

    x = list(range(1,cycles))
    plt.plot(x, fitnessResults)

    plt.xlabel('Games')
    plt.ylabel('Percentage wins')
    plt.show()