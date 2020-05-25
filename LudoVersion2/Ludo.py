import time
import numpy as np

import Player
import Board
import config
import Piece
import Dice
import PlayerData
# from Ludo64bitVersion import NNLudoPlayer
import AILudoPlayer


def doLudoMove(move, p, d, players):
    # Performe move
    movedPiece = (["MovePiece1", "MovePiece2","MovePiece3","MovePiece4"].index(move))

    if movedPiece >= 0:
        piece = p.pieces[movedPiece]
        if not piece.hasFinished:
            if piece.atHome and d == 6:
                piece.moveOutOnBoard(d)
            elif not piece.atHome:
                piece.move(d)
            else:
                if config.PRINT_NO_MOVE:
                    print("No move performed by player %s", (p.id))
        else:
            if config.PRINT_NO_MOVE:
                print("No move performed by player %s", (p.id))

    # Check if piece moved to a position owned by a piece from another player
    # If so move the other piece home
    for p2 in players:
        if p.id != p2.id:
            for piece in p2.pieces:
                if not piece.atHome and not piece.hasFinished and movedPiece != None and p.pieces[movedPiece].pos == piece.pos:
                    piece.moveHome()

class Ludo:
    def __init__(self, gameModes):
        self.noPlayers = len(gameModes)
        self.players = []
        self.gameModes = gameModes
        self.initializeNewPlayers()
        self.board = Board.Board()


    def initializeNewPlayers(self):
        PlayerData.reset()
        self.players = []
        for i in range(0, self.noPlayers):
            self.players.append(Player.Player(self.gameModes[i]))

    def configurePlayer(self, playerId, playerGamemode):
        self.players[playerId].gamemode = playerGamemode


    def runGame(self, AI, turns, gamesPerGeneration):
        aiWins = 0
        tieCount = 0
        allMoves = ["MovePiece1", "MovePiece2", "MovePiece3", "MovePiece4"]

        for game in range(0, gamesPerGeneration):
            # if game % 50 == 0:
            #     print("Game %s" % (str(game)))
            # Reset all players
            self.initializeNewPlayers()
            roundNumber = 0
            winner      = -1
            while winner == -1 and roundNumber < turns:
                for player in self.players:
                    # Roll Dice
                    dice = Dice.roll()

                    availableMoves = self.board.getAvailableMoves(player, dice)

                    move = None
                    if player.gamemode == "RA":
                        # Random player

                        # move = Piece.selectRandomMove(allMoves)
                        move = Piece.selectRandomMove(availableMoves)

                    elif player.gamemode == "AI":
                        # AI player
                        move = AI.getNextMove(allMoves, self.players, dice)

                    # Perform mode
                    doLudoMove(move, player, dice, self.players)

                    # Test if game is over
                    if player.hasWon():
                        winner = player.id
                        # if winner == 0:
                        #     print("AI win", end = ', ')
                        break
                roundNumber += 1
            if winner == 0:
                aiWins += 1
            if winner == -1:
                tieCount+= 1
        # print("Ties: %s" % (tieCount))
        # print("AI Wins: %s" % (aiWins))
        # print("Random Wins: %s" % (gamesPerGeneration-tieCount-aiWins))
        return aiWins,tieCount, gamesPerGeneration-tieCount-aiWins


    def play(self, gameId, pop, geneCount, turns, gamesPerGeneration):
        # Check if players are configured properly
        for p in self.players:
            if p.gamemode == None:
                assert False, "Player gamemode None is not a valid gamemode"

        populationSize = len(pop)
        populationResult = [None] * populationSize
        # populationFitness = np.zeros(populationSize)
        i = 0
        bestAiWin = 0
        bestTie = 0
        bestRandWin = 0
        for individual in pop:
            # print("Individual: #%s" % (str(i)))
            # Get AI player
            AI = AILudoPlayer.AILudoPlayer(geneCount, individual)

            # Run game
            [aiWins, ties, randWins] = self.runGame(AI, turns, gamesPerGeneration)

            # Save individual and its fitness
            # populationFitness[i] = aiWins/gamesPerGeneration
            populationResult[i] = ([{"fitness": aiWins/gamesPerGeneration, "DNA": individual}])

            # Keep track of the ties and rand wins for the best individual
            if bestAiWin < aiWins/gamesPerGeneration:
                bestAiWin = aiWins/gamesPerGeneration
                bestTie = ties
                bestRandWin = randWins
            i += 1

        # Sort list by fitness
        populationResult = sorted(populationResult, key=lambda k: k[0]['fitness'],reverse=True)


        return populationResult, bestTie, bestRandWin

