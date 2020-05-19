import random
import math
import time
import numpy as np

import Dice
import Player
import Board
import config
import Piece
import FileHandling as FH



import PlayerData

import NNLudoPlayer

totalFFTime = 0


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
            self.players.append(Player.Player())
            self.players[i].gamemode = self.gameModes[i]

    def configurePlayer(self, playerId, playerGamemode):
        self.players[playerId].gamemode = playerGamemode




    def runGame(self, diceThrows, maxRounds, NN):
        # Reset all players
        self.initializeNewPlayers()
        if config.PRINT_EXECUTION_TIME:
            global totalFFTime
        roundNumber = 0
        winner      = -1
        while winner == -1 and roundNumber < maxRounds:
            # Roll Dice
            d = diceThrows[roundNumber]
            for p in self.players:
                # Get available moves
                availableMoves = self.board.getAvailableMoves(p,d)
                allMoves = ["MovePiece1","MovePiece2","MovePiece3","MovePiece4"]
                if p.hasWon():
                    winner = p.id
                    if winner == 0 and config.PRINT_PLAYER_WINS:
                        print("NN Won")
                    break

                # Get board details
                board = self.board.getCurrentBoard(self.players)


                # Choose move from list
                move = None
                if p.gamemode == "RA":
                    # Random player
                    # move = Piece.selectRandomMove(availableMoves)
                    move = Piece.selectRandomMove(allMoves)
                elif p.gamemode == "NN":
                    # Neural network player
                    if config.PRINT_FF_TIME:
                        # Start generation timer
                        start = time.time()

                    # Get Neural Network mode
                    move = NN.getNextMove(allMoves, board, d, p)

                    if config.PRINT_FF_TIME:
                        # Stop and show generation time
                        end = time.time()
                        totalFFTime += (end - start) * 1000.00
                        # print("Feedforward Time: %s ms" % ((end - start) * 1000.00))
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

                if movedPiece >= 0: # and movedPiece <= self.noPlayers:
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
                for p2 in self.players:
                    if p.id != p2.id:
                        for piece in p2.pieces:
                            if not piece.atHome and not piece.hasFinished and movedPiece != None and p.pieces[movedPiece].pos == piece.pos:
                                piece.moveHome()
            roundNumber += 1
        if config.PRINT_ROUNDS_PLAYED:
            print("Rounds played: %s of %s" % (roundNumber, maxRounds))

        return self.players[0].getFitness(), winner

    def play(self, gameId, populationDNA, diceThrows, maxRounds):
        if config.PRINT_EXECUTION_TIME:
            global totalFFTime
            totalFFTime = 0

        # Check if players are configured properly
        for p in self.players:
            if p.gamemode == None:
                assert False, "Player gamemode None is not a valid gamemode"



        totalFitness = 0
        populationResult = []
        winners = np.zeros(5)
        # For each individual in population
        for individualDNA in populationDNA:
            # Get Neural Network from current individual
            NN = NNLudoPlayer.NNLudoPlayer(individualDNA)

            # Run game
            [fitness, winner] = self.runGame(diceThrows, maxRounds, NN)

            totalFitness += fitness
            winners[winner+1] += 1

            # Save individual and its fitness
            populationResult.append([{"fitness": fitness, "DNA": individualDNA}])

            # Optional print of fitness
            if config.PRINT_FITNESS_SCORES:
                print("Fitness: %s" % (str(fitness)))


        avgFitness = totalFitness/len(populationDNA)

        if config.PRINT_FF_TIME:
            print("FeedForward Time: %s ms" % (totalFFTime))

        # Sort list by fitness
        populationResult = sorted(populationResult, key=lambda k: k[0]['fitness'],reverse=True)

        # Return results
        # Best Fitnes, polulation result
        return populationResult[0][0]['fitness'], populationResult, winners, avgFitness


