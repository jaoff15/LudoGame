# Possible learning rewards:


import Piece

# This player gets it moves from a neural network
class NNLudoPlayer:
    def __init__(self):
        pass

    def getNextMove(self, availableMoves, board, dice, player, players):
        return Piece.selectRandomMove(availableMoves)