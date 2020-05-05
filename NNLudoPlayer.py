# Possible learning rewards:


import Piece
import NeuralNetwork.NeuralNetwork as NN

# This player gets it moves from a neural network
class NNLudoPlayer:
    def __init__(self):
        self.NN = NN.NeuralNetwork(65,65,2,4)

    def getNextMove(self, allMoves, board, dice, player, players):
        nnInput = self.NN.constructNNInput(board, dice, player, players)
        nnOutput = self.NN.ff(nnInput)
        assert nnOutput != None, "Output cannot be None"
        selectedMoveIndex = nnOutput.index(max(nnOutput))
        assert selectedMoveIndex >= 0, "Index cannot be negative"
        assert selectedMoveIndex <= 3, "Index cannot exceed 3"
        allMovesOrdered = self.__sortMoves(allMoves, player)
        selectedMove = allMovesOrdered[selectedMoveIndex]
        # print(nnOutput)
        # print(selectedMove)
        return Piece.selectRandomMove(allMoves)


    def __sortMoves(self, allmoves, player):
        # This function sorts the moves so the they are in the order of
        # how far along the track the piece is.
        # Finished pieces are at the front
        # Pieces at home are at the back

        pieces = {}
        for piece in player.pieces:
            if piece.hasFinished:
                pieces.update({piece.id: 200})
            elif piece.atHome:
                pieces.update({piece.id: -100})
            elif piece.onFinishStretch:
                pieces.update({piece.id: 100+piece.pos})
            else:
                pieces.update({piece.id: piece.pos})
        {k: v for k, v in sorted(pieces.items(), key=lambda item: item[1])}
        moves = []
        for m in pieces.keys():
            moves.append(allmoves[m-1])
        return moves

