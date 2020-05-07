import random
import math

import Player
import Board
import config
import Piece

import PlayerData

import MLudoPlayer
import SALudoPlayer
import NNLudoPlayer

class Ludo:
    def __init__(self, gameModes):

        self.noPlayers = len(gameModes)
        self.players = []
        for i in range(0,self.noPlayers):
            self.players.append(Player.Player())
            self.players[i].gamemode = gameModes[i]
        self.board = Board.Board()

    def configurePlayer(self, playerId, playerGamemode):
        self.players[playerId].gamemode = playerGamemode

    def reset(self):
        PlayerData.reset()

    def runGame(self, diceThrows, NN ):
        roundNumber = 0
        winner = None
        maxRounds = len(diceThrows)
        while winner == None and roundNumber < maxRounds:
            for p in self.players:
                # Roll Dice
                d = diceThrows[roundNumber]

                # Get available moves
                availableMoves = self.board.getAvailableMoves(p,d)
                allMoves = ["MovePiece1","MovePiece2","MovePiece3","MovePiece4"]
                if p.hasWon():
                    winner = p.id
                    break

                # Get board details
                board = self.board.getCurrentBoard(self.players)


                # Choose move from list
                move = None
                if p.gamemode == "RA":
                    # Choose random move
                    # m = random.randint(0, len(availableMoves) - 1)
                    # move = availableMoves[m]
                    move = Piece.selectRandomMove(availableMoves)
                # elif p.gamemode == "MA":
                #     # Let user choose the move
                #     pass
                # elif p.gamemode == "SA":
                #     # Let the simple automated player class choose the move
                #     move = SA.getNextMove(availableMoves, board, d, p, self.players)
                #     pass
                elif p.gamemode == "NN":
                        move = NN.getNextMove(allMoves, board, d, p, self.players)


                # Performe move
                movedPiece = None
                if move == "MovePiece1":
                    # p.pieces[0].move(d)
                    movedPiece = 0
                elif move == "MovePiece2":
                    # p.pieces[1].move(d)
                    movedPiece = 1
                elif move == "MovePiece3":
                    # p.pieces[2].move(d)
                    movedPiece = 2
                elif move == "MovePiece4":
                    # p.pieces[3].move(d)
                    movedPiece = 3
                else:
                    assert False, "Something went wrong"

                if movedPiece >= 0 and movedPiece <= self.noPlayers:
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




                # elif move == "MoveOutOfHome":
                #     if d == 6:
                #         for piece in p.pieces:
                #             movedPiece = piece.id-1
                #             if piece.atHome and not piece.hasFinished:
                #                 piece.moveOutOnBoard(d)
                #                 break
                # else:
                #     if config.PRINT_NO_MOVE:
                #         print("No move performed by player %s", (p.id))

                # Check if piece moved to a position owned by a piece from another player
                # If so move the other piece home
                for p2 in self.players:
                    if p.id != p2.id:
                        for piece in p2.pieces:
                            if not piece.atHome and not piece.hasFinished and movedPiece != None and p.pieces[movedPiece].pos == piece.pos:
                                piece.moveHome()
            roundNumber += 1
        return self.players[0].getFitness()

    def play(self, gameId, populationDNA):
        # Check if players are configured properly
        for p in self.players:
            if p.gamemode == None:
                assert False, "Player gamemode None is not a valid gamemode"

        # Enable gamemode classes
        # MA = MLudoPlayer.MLudoPlayer()
        # SA = SALudoPlayer.SALudoPlayer()


        # population = []
        # for individualDNA in populationDNA:
        #     population.append(NNLudoPlayer.NNLudoPlayer(individualDNA))
        #
        #
        #
        #     # NN = NNLudoPlayer.NNLudoPlayer(individualDNA)
        #     # population.append(NN)


        # for individualDNA in populationDNA
        #     NN = NNLudoPlayer.NNLudoPlayer(individualDNA)
        #     Run game with NN Player(using the lookup of the dice throw)
        #     Get fitness
        #     if fitness > bestFitness
        #       secondBestFitness = bestFitness
        #       secondBestDna =  bestDna
        #       bestFitness = fitness
        #       bestDna =  individualDna

        # Generate 'maxRounds' number of dice throws
        maxRounds   = max(10, math.floor(gameId))
        diceThrows = []
        for i in range(0,maxRounds):
            diceThrows.append(random.randint(1,6))

        bestFitness = 0
        bestIndividualDNA = None
        secondBestIndividualDNA = None

        for individualDNA in populationDNA:
            NN = NNLudoPlayer.NNLudoPlayer(individualDNA)
            fitness = self.runGame(diceThrows, NN)

            if fitness > bestFitness:
                secondBestIndividualDNA = bestIndividualDNA
                bestIndividualDNA = individualDNA
                bestFitness = fitness
                if config.PRINT_FITNESS_SCORES:
                    print("Fitness: %s" % (str(fitness)))

        return bestFitness, bestIndividualDNA, secondBestIndividualDNA


        # if config.PRINT_WINNER:
        #     print("Player %s has won!" % (winner))
        # if winner != None:
        #     return winner
        # else:
        #     return None
