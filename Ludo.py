import random
import math


import Player
import Board
import config
import Piece

import PlayerData

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
            # Roll Dice
            d = diceThrows[roundNumber]
            for p in self.players:
                # Get available moves
                availableMoves = self.board.getAvailableMoves(p,d)
                allMoves = ["MovePiece1","MovePiece2","MovePiece3","MovePiece4"]
                if p.hasWon():
                    winner = p.id
                    if winner == 0:
                        print("NN Won")
                    break

                # Get board details
                board = self.board.getCurrentBoard(self.players)


                # Choose move from list
                move = None
                if p.gamemode == "RA":
                    # Random player
                    move = Piece.selectRandomMove(availableMoves)
                elif p.gamemode == "NN":
                    # Neural network player
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
        return self.players[0].getFitness()

    def play(self, gameId, populationDNA):
        # Check if players are configured properly
        for p in self.players:
            if p.gamemode == None:
                assert False, "Player gamemode None is not a valid gamemode"

        # Generate 'maxRounds' number of dice throws
        maxRounds   = min(100, int(math.ceil(gameId / 10.0)) * 10)
        diceThrows = []
        for i in range(0,maxRounds):
            diceThrows.append(random.randint(1,6))


        populationResult = []
        # For each individual in population
        for individualDNA in populationDNA:
            # Get Neural Network from current individual
            NN = NNLudoPlayer.NNLudoPlayer(individualDNA)

            # Run game
            fitness = self.runGame(diceThrows, NN)

            # Save individual and its fitness
            populationResult.append([{"fitness": fitness, "DNA": individualDNA}])

            # Optional print of fitness
            if config.PRINT_FITNESS_SCORES:
                print("Fitness: %s" % (str(fitness)))



        # Sort list by fitness
        populationResult = sorted(populationResult, key=lambda k: k[0]['fitness'],reverse=True)

        # Reset player data to prepare for next game
        self.reset()

        # Return results
        # Best Fitnes, polulation result
        return populationResult[0][0]['fitness'], populationResult

