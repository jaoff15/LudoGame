
import Piece
import PlayerData
import config

POINTS_STEP                 = 1
POINTS_PIECE_FINISH         = 140
POINTS_PIECE_FINISHING_LANE = 10
POINTS_PIECE_AT_HOME        = -250
POINTS_INVALID_MOVE_CHOSEN  = -10


class Player:
    def __init__(self, gamemode=None):
        self.pieces = [None] * config.MAX_PIECES
        playerData = PlayerData.getPlayerData()
        self.id = playerData.id

        self.startPosition = playerData.startPosition
        self.endPosition = playerData.endPosition
        self.piecesFinished = 0

        # Used for fitness score
        # self.invalidMovesChosen = 0


        # gamemodes
        # None : Not configured. Will give an error
        # RA   : Random player. Move will be randomly selected from the available moves.
        # MA   : Manual Player. Moved will come from the user through the MLudoPlayer class
        # SA   : Simple Automated Player. Moves will be determined by the SALudoPlayer Class
        # NN   : Neural Network Player. Moved will be determined by the NNLudoPlayer class

        self.gamemode = gamemode
        self.__initializePlayer()

    def __initializePlayer(self):
        for i in range(1, config.MAX_PIECES+1):
            self.pieces[i-1] = Piece.Piece(self, i)

    def hasWon(self):
        return self.piecesFinished == 4

    def piecesAtHome(self):
        count = 0
        for p in self.pieces:
            if p.atHome:
                count+=1
        return count

    def getPiecesSorted(self):
        atGoal      = []
        isFinishing = []
        onBoard     = []
        atHome      = []
        for piece in self.pieces:
            # At goal
            if piece.hasFinished:
                atGoal.append(piece)
            # On finishing
            elif piece.onFinishStretch:
                isFinishing.append(piece)
            # At home
            elif piece.atHome:
                atHome.append(piece)
            # On board
            else:
                onBoard.append(piece)
        return atGoal + isFinishing + onBoard + atHome

    def getStartPos(self):
        return self.startPosition

    def getEndPos(self):
        return self.endPosition

    def getId(self):
        return self.id
