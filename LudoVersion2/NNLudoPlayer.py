import numpy as np

import Piece
from NeuralNetwork import NeuralNetwork as NN
from NeuralNetwork import DNA
import Ludo64bitVersion.config as config
import copy
import numpy as np
import Ludo as L

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

    def getNextMove(self, dice, Ludo):
        allMoves = ["MovePiece1", "MovePiece2", "MovePiece3", "MovePiece4"]
        nnResults = np.zeros(4)
        for i in range(0,len(allMoves)):
            move = allMoves[i]
            def getBoard1():
                # Make copy of Ludo game
                LudoCopy = copy.deepcopy(Ludo)
                # Perform move
                L.doLudoMove(move, LudoCopy.players[0], dice, LudoCopy.players)
                # Get board state
                return LudoCopy.getState()
            # board =getBoard1()

            def getBoard2():
                # Make copy of players
                copiedPlayers = copy.deepcopy(Ludo.players)
                # Do move on copied players
                L.doLudoMove(move, copiedPlayers[0], dice, copiedPlayers)
                # Get histogram of ludo board
                ludoHistogram = Ludo.board.getHistogram()
                # Get board status after current move
                boardAfterMove = Ludo.board.getBoardStatus(copiedPlayers)
                # Return histogram after move
                return ludoHistogram+boardAfterMove

            board = getBoard2()
            # Construct NN input
            nnInput = board.flatten()
            # Run NN feedforward
            nnOutput = self.NN.ff(nnInput)
            # Load output
            nnResults[i] = nnOutput[0]

        # Find and return index of max value
        return allMoves[np.argmax(nnResults)]



    # def getNextMove(self, allMoves, board, dice, player):
    #     # Create Neural Network Input signal
    #     nnInput = self.NN.constructNNInput(board, dice, player)
    #     # Get Neural Network Output
    #     nnOutput = self.NN.ff(nnInput)
    #
    #     if config.ENABLE_CHECKS:
    #         assert len(nnOutput) != 0, "Output cannot be None"
    #
    #     # Translate neural network output to a move index
    #     # selectedMoveIndex = nnOutput.index(max(nnOutput))
    #     selectedMoveIndex = np.argmax(nnOutput)
    #     if config.ENABLE_CHECKS:
    #         assert selectedMoveIndex >= 0, "Index cannot be negative"
    #         assert selectedMoveIndex <= 3, "Index cannot exceed 3"
    #
    #     # Order the available moves so the first index is the piece the furthest along the board
    #     allMovesOrdered = self.__sortMoves(allMoves, player)
    #
    #     # Select move from ordered list
    #     selectedMove = allMovesOrdered[selectedMoveIndex]
    #
    #     # Select move from possible moves
    #     # selectedMove = allMoves[selectedMoveIndex]
    #     return selectedMove
    #
    #
    #
    # def __sortMoves(self, allmoves, player):
    #     # This function sorts the moves so the they are in the order of
    #     # how far along the track the piece is.
    #     # Finished pieces are at the front
    #     # Pieces at home are at the back
    #
    #     pieces = {}
    #     for piece in player.pieces:
    #         if piece.hasFinished:
    #             pieces.update({piece.id: -200})
    #             # pass
    #         elif piece.atHome:
    #             pieces.update({piece.id: -100})
    #         elif piece.onFinishStretch:
    #             pieces.update({piece.id: 100+piece.pos})
    #         else:
    #             pieces.update({piece.id: piece.pos})
    #     pieces = sorted(pieces.items(), key=lambda x: x[1], reverse=True)
    #     # {k: v for k, v in sorted(pieces.items(), key=lambda item: item[1])}
    #     moves = [None]*4
    #     for i in range(0, len(pieces)):
    #     # for m in pieces:
    #         moves[i] = allmoves[pieces[i][0]-1]
    #     return moves

