

import Ludo




if __name__ == '__main__':
    noGames = 10
    noPlayers = 2
    gameModes = ["RA", "SA"]
    winners = []
    for i in range(1, noGames):
        ludo = Ludo.Ludo(noPlayers)
        for p in range(0, noPlayers):
            ludo.configurePlayer(p, gameModes[p])
        # ludo.configurePlayer(0, "SA")
        # ludo.configurePlayer(1, "RA")
        winner = ludo.play()
        ludo.reset()
        winners.append(winner)

    for p in range(0,noPlayers):
        count = winners.count(p)
        print("Player %s in gamemode '%s' won %s amount of times" % (p, gameModes[p], count))

    # print(winners)