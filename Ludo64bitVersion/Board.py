
from Ludo64bitVersion import config
from Ludo64bitVersion import Piece
import math
import numpy as np

class Board:
    def __init__(self):
        self.histogram = np.zeros((2,1 + config.MAX_POSITIONS+config.MAX_FINISH_LANE_POSITIONS + 1))

    def boardReset(self):
        self.histogram = np.zeros((2,1 + config.MAX_POSITIONS+config.MAX_FINISH_LANE_POSITIONS + 1))

    def getAvailableMoves(self, player, steps):
        # Check the following moves
        #   Move Piece 1 forward
        #   Move Piece 2 forward
        #   Move Piece 3 forward
        #   Move Piece 4 forward
        #   REMOVED: Move Piece out of Home
        availableMoves = []

        # Check each piece if it can move forward
        index = 1
        for piece in player.pieces:
            # Check if the piece is out on the board
            isAvailable = not piece.atHome and not piece.hasFinished
            if isAvailable:
                # Check if moving piece the amount of steps found by the dice
                # would bring it to a position that is already occupied by a piece from the same player
                for otherPiece in player.pieces:
                    if otherPiece.id is not piece.id:
                        if otherPiece.pos == (piece.pos + steps) % config.MAX_POSITIONS and not otherPiece.hasFinished:
                            isAvailable = False
                            break
                    if not isAvailable:
                        break
                if isAvailable:
                    availableMoves.append("MovePiece"+str(index))
            index += 1

        return availableMoves

    def getFullBoard(self, players):
        board = np.zeros((len(players),1 + config.MAX_POSITIONS+config.MAX_FINISH_LANE_POSITIONS + 1))
        pieceAmount = 0.25
        for i in range(0,len(players)):
            for piece in players[i].pieces:
                if piece.atHome:
                    board[i][0] += pieceAmount
                elif piece.hasFinished:
                    board[i][-1] += pieceAmount
                elif piece.onFinishStretch:
                    board[i][1 + config.MAX_POSITIONS+ math.floor(piece.pos)] += pieceAmount
                else:
                    board[i][math.floor(piece.pos)] += pieceAmount
        return board
    def getSemiFullBoard(self, players):
        board = np.zeros((2,1 + config.MAX_POSITIONS+config.MAX_FINISH_LANE_POSITIONS + 1))
        pieceAmount = 1/12
        for i in range(0,len(players)):
            for piece in players[i].pieces:
                p = 0 if i == 0 else 1
                if piece.atHome:
                    board[p][0] += pieceAmount
                elif piece.hasFinished:
                    board[p][-1] += pieceAmount
                elif piece.onFinishStretch:
                    board[p][1 + config.MAX_POSITIONS+ math.floor(piece.pos)] += pieceAmount
                else:
                    board[p][math.floor(piece.pos)] += pieceAmount
        return board

    def getBoardStatus(self, players):
        board = np.zeros((2,1 + config.MAX_POSITIONS+config.MAX_FINISH_LANE_POSITIONS + 1))
        pieceAmount = 1 / 100
        for i in range(0, len(players)):
            for piece in players[i].pieces:
                p = 0 if i == 0 else 1
                if piece.atHome:
                    board[p][0] += pieceAmount
                elif piece.hasFinished:
                    board[p][-1] += pieceAmount
                elif piece.onFinishStretch:
                    board[p][1 + config.MAX_POSITIONS + math.floor(piece.pos)] += pieceAmount
                else:
                    board[p][math.floor(piece.pos)] += pieceAmount
        return board

    def updateHistogram(self, players):
        currentBoard = self.getBoardStatus(players)
        self.histogram += currentBoard
        assert 1 not in self.histogram, "Descrease piece amount"


    # def updateAndGetHistogram(self, players):
    #     self.updateHistogram(players)
    #     return self.histogram

    def getHistogram(self):
        return self.histogram


    # def getCurrentBoard(self, players):
    #     # Return an array containing all board positions
    #     # 0 = No player on position
    #     # 1 = Position contains a piece
    #     board = np.zeros(config.MAX_POSITIONS)
    #     for p in players:
    #         for piece in p.pieces:
    #             if not piece.hasFinished and not piece.atHome:
    #                 board[math.floor(piece.pos)-1] = 1
    #     return board