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
    def __init__(self, noPlayers):

        self.noPlayers = noPlayers
        self.players = []
        for i in range(1,self.noPlayers+1):
            self.players.append(Player.Player())
        self.board = Board.Board()

    def configurePlayer(self, playerId, playerGamemode):
        self.players[playerId].gamemode = playerGamemode

    def reset(self):
        PlayerData.reset()

    def play(self, gameId, populationDNA):
        # Check if players are configured properly
        for p in self.players:
            if p.gamemode == None:
                assert False, "Player gamemode None is not a valid gamemode"

        # Enable gamemode classes
        MA = MLudoPlayer.MLudoPlayer()
        SA = SALudoPlayer.SALudoPlayer()

        population = []
        for individualDNA in populationDNA:
            population.append(NNLudoPlayer.NNLudoPlayer(individualDNA))



            # NN = NNLudoPlayer.NNLudoPlayer(individualDNA)
            # population.append(NN)

        maxRounds = max(10, math.floor(gameId))
        winner = None
        roundNumber = 0
        while winner == None and roundNumber < maxRounds:
            roundNumber += 1
            for p in self.players:
                # Roll Dice
                d = random.randint(1,6)

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
                elif p.gamemode == "MA":
                    # Let user choose the move
                    pass
                elif p.gamemode == "SA":
                    # Let the simple automated player class choose the move
                    move = SA.getNextMove(availableMoves, board, d, p, self.players)
                    pass
                elif p.gamemode == "NN":
                    for individual in population:
                        #TODO Fix situation with multiple parallel games
                        # Let the neural network player choose the move
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

        bestFitness = 0
        bestIndividual = None
        secondBestIndividual = None
        if config.PRINT_FITNESS_SCORES:
            for individual in population:
                fitness = individual.getFitness()
                if fitness > bestFitness:
                    secondBestIndividual = bestIndividual
                    bestIndividual = individual
                    bestFitness = fitness
            # for p in self.players:
            #
            #     print(p.getFitness())
            print("Player %s fitness: %s" %( p.id, str(p.getFitness())))

        return bestFitness, bestIndividual, secondBestIndividual
        # if config.PRINT_WINNER:
        #     print("Player %s has won!" % (winner))
        # if winner != None:
        #     return winner
        # else:
        #     return None
