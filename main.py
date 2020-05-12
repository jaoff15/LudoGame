
import Ludo
import matplotlib.pyplot as plt
from NeuralNetwork import NeuralNetwork as NN
import config


# This function performs a game of Ludo
def runGame(gameModes,gameId, popualationSize):
    # Get a Ludo game
    ludo = Ludo.Ludo(gameModes)

    # Create a new generation
    populationDNA =  NN.createPopulation(popualationSize)

    # Play the Ludo game with the current population
    [bestFitness, populationResult] = ludo.play(gameId, populationDNA)

    # Save the fitness results from the ludo game
    NN.saveLastPolulation(populationResult)

    return bestFitness



if __name__ == '__main__':
    gameModes = ["NN", "RA", "RA", "RA"]

    cycles          = 100 # How many times should the ludo game be played
    fitnessResults  = [] # Array to hold result from the games
    fitnessResultsAvg = []
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
        lf = len(fitnessResults)
        if lf > 10:
            sum = 0
            for i in range(lf-10,lf):
                sum += fitnessResults[i]
            fitnessResultsAvg.append(sum/10)


    plt.subplot(2, 1, 1)
    x = list(range(0, len(fitnessResults)))
    plt.plot(x, fitnessResults)
    plt.xlabel('Games')
    plt.ylabel('Fitness score')


    plt.subplot(2, 1, 2)
    x2 = list(range(0, len(fitnessResultsAvg)))
    plt.plot(x2, fitnessResultsAvg)
    plt.xlabel('Games')
    plt.ylabel('Fitness score rolling average of last 10 games')
    plt.show()