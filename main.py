
import Ludo
import matplotlib.pyplot as plt


def benchMark(noPlayers, gameModes):
    noGames = 100

    winners = []
    for i in range(0, noGames):
        ludo = Ludo.Ludo(noPlayers)
        for p in range(0, noPlayers):
            ludo.configurePlayer(p, gameModes[p])
        winner = ludo.play()
        ludo.reset()
        winners.append(winner)

    # for p in range(0, noPlayers):
    #     count = winners.count(p)
    #     print("Player %s in gamemode '%s' won %s amount of times" % (p, gameModes[p], count))
    # print("Total number of games: " + str(noGames))
    return (winners.count(3)/noGames)*100


if __name__ == '__main__':
    noPlayers = 4
    gameModes = ["RA", "RA", "RA", "NN"]

    games = 40
    gamesBetweenBenchmarks = 10
    results = []

    for game in range(1, games + 1):
        # Train neutral network


        # Perform bench mark
        if game % gamesBetweenBenchmarks == 0:
            results.append(benchMark(noPlayers, gameModes))

    x = list(range(0, games, gamesBetweenBenchmarks))
    plt.plot(x, results)

    plt.title("Neural Network Performance (Percentage wins out of 100 games)")
    plt.xlabel('Games')
    plt.ylabel('Percentage wins')
    plt.show()