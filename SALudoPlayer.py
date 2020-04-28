
import Piece
import random
# Simple Automated Ludo Player


class SALudoPlayer:
    def __init__(self):
        pass

    def getNextMove(self, availableMoves, board, dice, player, players):
        # Priority:
        #   Move piece to position of piece owned by other player
        #   Move piece out of position where other player can knock it home
        #   Move pieces to finish lane
        #   Move pieces out of home
        #   Move piece towards finishing lane
        #   Move piece to goal


        playerPiecePositions = []
        for piece in player.pieces:
            if not piece.atHome or piece.hasFinished:
                playerPiecePositions.append(piece.pos)

        positionIndex = 1
        for position in board:
            if position == "Piece":
                for piece in player.pieces:

                    # Make sure piece has not finished, is not still in the home base, is not on the finishing lane
                    # and is the one actually owning the current position
                    if not piece.hasFinished and not piece.atHome and not piece.onFinishStretch and positionIndex == piece.pos:
                        # Find the next position that piece would go to
                        [nextPos, willFinish] = Piece.getNextPos(piece.pos, dice, piece.stepsMoved)
                        if not willFinish and nextPos not in playerPiecePositions:
                            if board[nextPos-1] == "Piece" and board[nextPos-1] not in playerPiecePositions:
                                # Piece is able to a position owned by another player
                                # print("Moving piece %s to position %s to knock home opponent piece" % (piece.id, nextPos))
                                # Make sure moving piece is a legit move
                                assert  "MovePiece" + str(piece.id) in availableMoves, "Something went wrong"
                                return "MovePiece" + str(piece.id)

            positionIndex += 1
        #   Move piece out of position where other player can knock it home



        return Piece.selectRandomMove(availableMoves)