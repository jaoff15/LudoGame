import time


import Ludo
import matplotlib.pyplot as plt
from NeuralNetwork import NeuralNetwork as NN
import config
import FileHandling as FH
from NeuralNetwork import DNA

gWeightsFileName = "weights.csv"
gFitnessFileName = "fitness.csv"
gFitnessAvgFileName = "fitness_avg.csv"
gWinPercentFileName = "win_percent.csv"

# Done Improve individual selection weights
# Done Save model weights to csv
# Done Save fitness data to csv
# Done Create performance test. Every N games the best individual from last population is put into a turnament of N2 games and the win percentage is logged to a file

gMAX_FITNESS = 1000
def testPerformance(noGames, individual):

    noWins = 0
    for i in range(0, noGames):
        # Get a Ludo game
        ludo = Ludo.Ludo(gameModes)

        # Play the Ludo game with individual
        [fitness, result] = ludo.play(gameId, [individual])
        global gMAX_FITNESS
        if fitness >= gMAX_FITNESS:
            noWins += 1

    winPercent = (noWins/noGames) * 100.00
    return winPercent


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
    # Log Time
    start = time.time()

    # Create files
    weightsFile = FH.makeNewFile(gWeightsFileName)
    fitnessFile = FH.makeNewFile(gFitnessFileName)
    fitnessAvgFile = FH.makeNewFile(gFitnessAvgFileName)
    winPercentFile = FH.makeNewFile(gWinPercentFileName)



    gameModes = ["NN", "RA", "RA", "RA"]

    cycles          = 20 # How many times should the ludo game be played
    gameId          = 1  # A way to lookup how many games has been performed
    populationSize  = 100  # How many individuals should the population contain
    fitnessResults  = [] # Array to hold result from the games
    fitnessResultsAvg = []


    winPercent          = []
    cyclesBetweenTests  = 100
    testCycles          = 100

    for cycle in range(1, cycles + 1):
        print("\nGeneration: #%s" % (cycle))

        # Run game
        bestFitness = runGame(gameModes, gameId, populationSize)

        # Save fitness results
        FH.appendToFile(fitnessFile, (str(gameId) + ',' + str(bestFitness)))

        if config.PRINT_BEST_FITNESS_SCORE:
            print("Best Fitness: %s", (bestFitness))



        # Handle Analysis
        gameId += 1
        fitnessResults.append(bestFitness)
        # Rolling average
        lf = len(fitnessResults)
        if lf > 10:
            sum = 0
            for i in range(lf-10,lf):
                sum += fitnessResults[i]
            fitnessResultsAvg.append(sum/10)
            # Save fitness results
            FH.appendToFile(fitnessAvgFile, (str(gameId) + ',' + str(fitnessResultsAvg[-1])))

        # Get best individual
        bestIndividual = NN.getBestIndividual()

        # Write best individual to file
        FH.writeToFile(weightsFile, DNA.toStr(bestIndividual))

        # Once in a while make a performance test of the last best individual
        if cycle % cyclesBetweenTests == 0:
            # Perform tests
            if bestIndividual is not None:
                winPercent.append(testPerformance(testCycles, bestIndividual))
                print("Win percent %s" % (winPercent[-1]))
                # Write result to file
                FH.appendToFile(winPercentFile, (str(gameId) + ',' + str(winPercent[-1])))


    # Time measurement
    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Executing Time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))



    # Plotting
    plt.subplot(3, 1, 1)
    if len(fitnessResults) != 0:
        x = list(range(0, len(fitnessResults)))
        plt.plot(x, fitnessResults)
        plt.xlabel('Games')
        plt.ylabel('Fitness score')

    plt.subplot(3, 1, 2)
    if len(fitnessResultsAvg) != 0:
        x2 = list(range(0, len(fitnessResultsAvg)))
        plt.plot(x2, fitnessResultsAvg)
        plt.xlabel('Games')
        plt.ylabel('Fitness score rolling average of last 10 games')

    plt.subplot(3, 1, 3)
    if len(winPercent) != 0:
        x3 = list(range(0, len(winPercent)))
        plt.plot(x3, winPercent)
        # plt.xlabel('%s Games' % (cyclesBetweenTests))
        plt.ylabel('Win percentage of %s games' % (testCycles))

    plt.show()