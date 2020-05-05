
import Ludo
import matplotlib.pyplot as plt


def runNGames(noPlayers, gameModes, noGames):
    print("Benchmark...")

    winners = []
    for i in range(0, noGames):
        print("B%s"%(i))
        ludo = Ludo.Ludo(noPlayers)
        for p in range(0, noPlayers):
            ludo.configurePlayer(p, gameModes[p])
        winner = ludo.play()
        ludo.reset()
        winners.append(winner)

    return (winners.count(3)/noGames)*100


if __name__ == '__main__':
    noPlayers = 4
    gameModes = ["NN", "RA", "RA", "RA"]

    cycles = 10
    gamesPerCycle = 20
    results = []


    for cycle in range(1, cycles + 1):
        print("Cycle: #%s" % (cycle))
        # Train neutral network

        # Run games some times
        result = runNGames(noPlayers, gameModes, gamesPerCycle)
        print(result)
        results.append(result)

    x = list(range(gamesPerCycle, (cycles+1)*gamesPerCycle, gamesPerCycle))
    plt.plot(x, results)

    plt.title("Neural Network Performance (Percentage wins of the last %s games)" % (gamesPerCycle))
    plt.xlabel('Games')
    plt.ylabel('Percentage wins')
    plt.show()