import numpy as np
from numba import jit
import random

@jit(nopython=True)
def getRandomNumb():
    # Range [-1,1]
    return (2 * random.random()) - 1

class AILudoPlayer():
    def __init__(self,geneCount, genes = []):
        self.geneCount = geneCount
        self.pieceCount = 4
        self.genes = genes
        # if len(individualDNA) == 0:
        #     self.genes = np.random.rand(self.geneCount*self.pieceCount)
        # else:
        assert self.geneCount*self.pieceCount == len(genes), "genes needs to be the correct length"


    def getNextMove(self, allMoves, players, dice):
        pieceCount = len(players[0].pieces)
        otherPlayers = players[1:4]

        piecesSorted = players[0].getPiecesSorted()

        currentStatus = np.zeros((4, self.geneCount))
        for i in range(0, pieceCount):
            piece = piecesSorted[i]

            # Version 1
            piece.updateSurroundings(otherPlayers)
            # Good
            currentStatus[i][0] = 1 if piece.atHome and dice == 6                   else 0
            currentStatus[i][1] = 1 if piece.willHitGoal(dice)                      else 0
            currentStatus[i][2] = 1 if piece.willKnockHomeEnemy(dice, otherPlayers) else 0
            currentStatus[i][3] = 1 if piece.willMoveToLessDangerousPos(dice)      else 0
            currentStatus[i][4] = 1 if piece.willMoveWithinKnockingDistance(dice)   else 0
            # Bad
            currentStatus[i][5] = 1 if piece.willMoveToMoreDangerousPos(dice)       else 0
            currentStatus[i][6] = 1 if piece.willBounceOffGoal(dice)                else 0
            # Bias
            # currentStatus[i][7] = 0.25 * i # Piece order
            currentStatus[i][7] = 1

            # currentStatus[i][0] = 1 if piece.atHome and dice == 6 else 0
            # currentStatus[i][1] = 1 if piece.willHitGoal(dice) else 0
            # currentStatus[i][2] = 1 if piece.willBounceOffGoal(dice) else 0
            #
            # piece.updateSurroundings(otherPlayers)
            # behindNow    = piece.behind[0:6]
            # infrontNow   = piece.infront[0:6]
            # behindAfter  = piece.behind[dice:6+dice]
            # infrontAfter = piece.behind[dice:6 + dice]
            # currentStatus[i][3:9]   = behindNow
            # currentStatus[i][9:15]  = behindAfter
            # currentStatus[i][15:21] = infrontNow
            # currentStatus[i][21:27] = infrontAfter
            # currentStatus[i][27] = 1

        actionScores  = np.multiply(self.genes.reshape(currentStatus.shape), currentStatus)
        pieceScores   = np.sum(actionScores,1)
        selectedPiece = np.argmax(pieceScores)

        moveIndex = piecesSorted[selectedPiece].id - 1

        return allMoves[moveIndex]
