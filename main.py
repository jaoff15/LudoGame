
import Ludo
import matplotlib.pyplot as plt
from NeuralNetwork import NeuralNetwork as NN

def runNGames(noPlayers, gameModes, noGames,gameId, popualationSize):
    print("Benchmark...")

    winners = []
    bestIndividual = None
    secondBestIndividual = None
    for i in range(0, noGames):
        print("B%s"%(i))
        ludo = Ludo.Ludo(noPlayers)
        for p in range(0, noPlayers):
            ludo.configurePlayer(p, gameModes[p])
        populationDNA =  NN.createPopulation(populationSize,bestIndividual, secondBestIndividual)

        [bestFitness, bestIndividual, secondBestIndividual] = ludo.play(gameId, populationDNA)
        ludo.reset()
        # winners.append(winner)
    return bestFitness
    # return (winners.count(3)/noGames)*100


if __name__ == '__main__':
    noPlayers = 4
    gameModes = ["NN", "RA", "RA", "RA"]

    cycles = 10
    gamesPerCycle = 20
    results = []
    gameId = 0
    populationSize = 10

    for cycle in range(1, cycles + 1):
        print("Cycle: #%s" % (cycle))
        # Train neutral network

        # Run games some times

        bestFitness = runNGames(noPlayers, gameModes, gamesPerCycle, gameId,populationSize)
        # print(result)
        # results.append(result)
        gameId += 1

    x = list(range(gamesPerCycle, (cycles+1)*gamesPerCycle, gamesPerCycle))
    plt.plot(x, results)

    plt.title("Neural Network Performance (Percentage wins of the last %s games)" % (gamesPerCycle))
    plt.xlabel('Games')
    plt.ylabel('Percentage wins')
    plt.show()