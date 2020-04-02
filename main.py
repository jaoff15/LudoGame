

import Ludo




if __name__ == '__main__':
    noGames = 10
    noPlayers = 4
    gameModes = ["RA", "RA", "SA", "RA"]
    winners = []
    for i in range(0, noGames):
        ludo = Ludo.Ludo(noPlayers)
        for p in range(0, noPlayers):
            ludo.configurePlayer(p, gameModes[p])
        winner = ludo.play()
        ludo.reset()
        winners.append(winner)

    for p in range(0,noPlayers):
        count = winners.count(p)
        print("Player %s in gamemode '%s' won %s amount of times" % (p, gameModes[p], count))
    print("Total number of games: " + str(noGames))
    # print(winners)