
import config
import Piece
import math
import numpy as np

class Board:
    def __init__(self):
        pass


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



    def getCurrentBoard(self, players):
        # Return an array containing all board positions
        # 0 = No player on position
        # 1 = Position contains a piece
        board = np.zeros(config.MAX_POSITIONS)
        for p in players:
            for piece in p.pieces:
                if not piece.hasFinished and not piece.atHome:
                    board[math.floor(piece.pos)-1] = 1
        return board