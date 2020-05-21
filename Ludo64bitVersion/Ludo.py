import time
import numpy as np

from Ludo64bitVersion import Player
from Ludo64bitVersion import Board
from Ludo64bitVersion import config
from Ludo64bitVersion import Piece
from Ludo64bitVersion import PlayerData
from Ludo64bitVersion import NNLudoPlayer

totalFFTime = 0


def doLudoMove(move, p, d, players):
    # Performe move
    movedPiece = (["MovePiece1", "MovePiece2","MovePiece3","MovePiece4"].index(move))-1
    # if move == "MovePiece1":
    #     movedPiece = 0
    # elif move == "MovePiece2":
    #     movedPiece = 1
    # elif move == "MovePiece3":
    #     movedPiece = 2
    # elif move == "MovePiece4":
    #     movedPiece = 3
    # else:
    #     assert False, "Something went wrong"

    if movedPiece >= 0:  # and movedPiece <= self.noPlayers:
        piece = p.pieces[movedPiece]
        if not piece.hasFinished:
            if piece.atHome and d == 6:
                piece.moveOutOnBoard(d)
            elif not piece.atHome:
                piece.move(d)
            else:
                p.incInvalidMoveChosen()
                if config.PRINT_NO_MOVE:
                    print("No move performed by player %s", (p.id))
        else:
            p.incInvalidMoveChosen()
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




    def getState(self):
        # return self.board.getFullBoard(self.players)
        # return self.board.getSemiFullBoard(self.players)
        self.board.updateHistogram(self.players)
        return self.board.getHistogram()


    def runGame(self, diceThrows, maxRounds, NN):
        # Reset all players
        self.initializeNewPlayers()
        self.board.boardReset()
        if config.PRINT_EXECUTION_TIME:
            global totalFFTime
        roundNumber = 0
        winner      = -1
        while winner == -1 and roundNumber < maxRounds:
            # Roll Dice
            dice = diceThrows[roundNumber]
            for player in self.players:

                move = None
                if player.gamemode == "RA":
                    # Random player
                    # availableMoves = self.board.getAvailableMoves(player, dice)
                    # move = Piece.selectRandomMove(availableMoves)
                    allMoves = ["MovePiece1", "MovePiece2", "MovePiece3", "MovePiece4"]
                    move = Piece.selectRandomMove(allMoves)
                elif player.gamemode == "NN":
                    # Neural network player

                    if config.PRINT_FF_TIME:
                        # Start generation timer
                        start = time.time()

                    # Get Neural Network mode
                    move = NN.getNextMove(dice, self)
                    # move = NN.getNextMove(self)

                    if config.PRINT_FF_TIME:
                        # Stop and show generation time
                        end = time.time()
                        totalFFTime += (end - start) * 1000.00

                # Perform mode
                doLudoMove(move, player, dice, self.players)

                # Test if game is over
                if player.hasWon():
                    winner = player.id
                    if winner == 0 and config.PRINT_PLAYER_WINS:
                        print("NN Won")
                    break
            roundNumber += 1
        if config.PRINT_ROUNDS_PLAYED:
            print("Rounds played: %s of %s" % (roundNumber, maxRounds))



        # randPlayerFitness = [self.players[1].getFitness(),self.players[2].getFitness(),self.players[3].getFitness()]
        # avgRandomPlayerFitness = sum(randPlayerFitness)/3
        # maxRandomPlayerFitness = max(randPlayerFitness)
        # randomPlayerData = {'avg':avgRandomPlayerFitness, 'max':maxRandomPlayerFitness}

        # Update histrogram and calcualte the player fitness
        self.board.updateHistogram(self.players)
        fitnessData = self.calculateFitnessScores()

        # return self.players[0].getFitness(), winner, randomPlayerData

        return winner, fitnessData

    def calculateFitnessScores(self):
        p0 = np.dot(self.board.histogram[0], np.arange(len(self.board.histogram[0])))*2
        p1 = np.dot(self.board.histogram[1], np.arange(len(self.board.histogram[1])))/3
        finish = self.players[0].piecesFinished * 10
        # home = self.players[0].piecesAtHome()
        fitness = (finish + p0) - (p1)
        return {"AI":fitness}

    def play(self, gameId, populationDNA, diceThrows, maxRounds):
        if config.PRINT_EXECUTION_TIME:
            global totalFFTime
            totalFFTime = 0

        # Check if players are configured properly
        for p in self.players:
            if p.gamemode == None:
                assert False, "Player gamemode None is not a valid gamemode"



        # totalFitness = 0
        # totalRandomPlayerData = {'avg': 0, 'max':-1000}
        populationSize = len(populationDNA)
        populationResult = [None] * populationSize
        populationFitnessData = np.zeros(populationSize)
        winners = np.zeros(5)
        # For each individual in population
        i = 0
        for individualDNA in populationDNA:
            # Get Neural Network from current individual
            NN = NNLudoPlayer.NNLudoPlayer(individualDNA)

            # Run game
            [winner, fitnessData] = self.runGame(diceThrows, maxRounds, NN)

            # totalRandomPlayerData['avg'] += randomPlayerData['avg']
            # totalRandomPlayerData['max'] = max(totalRandomPlayerData['max'], randomPlayerData['max'])
            # totalFitness += fitnessData["AI"]
            winners[winner+1] += 1

            # Save individual and its fitness
            populationResult[i] = ([{"fitness": fitnessData["AI"], "DNA": individualDNA}])
            populationFitnessData[i] = fitnessData["AI"]
            # Optional print of fitness
            if config.PRINT_FITNESS_SCORES:
                print("Fitness: %s" % (str(fitnessData["AI"])))
            i += 1

        # avgFitness = totalFitness/populationSize
        # totalRandomPlayerData['avg'] = totalRandomPlayerData['avg']/populationSize

        if config.PRINT_FF_TIME:
            print("FeedForward Time: %s ms" % (totalFFTime))

        # Sort list by fitness
        populationResult = sorted(populationResult, key=lambda k: k[0]['fitness'],reverse=True)

        # Return results
        # Best Fitnes, polulation result
        # return populationResult[0][0]['fitness'], populationResult, winners, avgFitness, totalRandomPlayerData
        playerFitnessData = {"max":np.max(populationFitnessData),"avg":np.average(populationFitnessData),"min":np.min(populationFitnessData)}
        # return populationResult[0][0]['fitness'], populationResult, winners, avgFitness
        return playerFitnessData, populationResult, winners

