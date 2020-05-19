import numpy as np

import Piece
import NeuralNetwork.NeuralNetwork as NN
from NeuralNetwork import DNA
import config

# This player gets it moves from a neural network
class NNLudoPlayer:
    def __init__(self,individualDNA = None):

        if len(individualDNA) != 0:
            dna = DNA.DNA()
            [wInput, wBiasInput, wHidden, wBiasHidden, wOutput, wBiasOutput] = dna.extractFromDNA(individualDNA,NN.INPUT_NEURONS, NN.HIDDEN_NEURONS_PER_LAYER, NN.HIDDEN_LAYERS, NN.OUTPUT_NEURONS)
            self.NN = NN.NeuralNetwork(NN.INPUT_NEURONS, NN.HIDDEN_NEURONS_PER_LAYER, NN.HIDDEN_LAYERS, NN.OUTPUT_NEURONS,
                                       inputWeights=wInput, inputBiasWeights=wBiasInput,
                                       hiddenWeights=wHidden, hiddenBiasWeights=wBiasHidden,
                                       outputWeights=wOutput,outputBiasWeights=wBiasOutput)
        else:
            self.NN = NN.NeuralNetwork(NN.INPUT_NEURONS, NN.HIDDEN_NEURONS_PER_LAYER, NN.HIDDEN_LAYERS, NN.OUTPUT_NEURONS)

    def getNextMove(self, allMoves, board, dice, player):
        # Create Neural Network Input signal
        nnInput = self.NN.constructNNInput(board, dice, player)
        # Get Neural Network Output
        nnOutput = self.NN.ff(nnInput)

        if config.ENABLE_CHECKS:
            assert len(nnOutput) != 0, "Output cannot be None"

        # Translate neural network output to a move index
        # selectedMoveIndex = nnOutput.index(max(nnOutput))
        selectedMoveIndex = np.argmax(nnOutput)
        if config.ENABLE_CHECKS:
            assert selectedMoveIndex >= 0, "Index cannot be negative"
            assert selectedMoveIndex <= 3, "Index cannot exceed 3"

        # Order the available moves so the first index is the piece the furthest along the board
        # allMovesOrdered = self.__sortMoves(allMoves, player)

        # Select move from ordered list
        # selectedMove = allMovesOrdered[selectedMoveIndex]

        # Select move from possible moves
        selectedMove = allMoves[selectedMoveIndex]
        return selectedMove



    def __sortMoves(self, allmoves, player):
        # This function sorts the moves so the they are in the order of
        # how far along the track the piece is.
        # Finished pieces are at the front
        # Pieces at home are at the back

        pieces = {}
        for piece in player.pieces:
            if piece.hasFinished:
                pieces.update({piece.id: -200})
                # pass
            elif piece.atHome:
                pieces.update({piece.id: -100})
            elif piece.onFinishStretch:
                pieces.update({piece.id: 100+piece.pos})
            else:
                pieces.update({piece.id: piece.pos})
        pieces = sorted(pieces.items(), key=lambda x: x[1], reverse=True)
        # {k: v for k, v in sorted(pieces.items(), key=lambda item: item[1])}
        moves = []
        for m in pieces:
            moves.append(allmoves[m[0]-1])
        return moves

