
from Ludo64bitVersion import Piece
from Ludo64bitVersion import PlayerData
from Ludo64bitVersion import config

POINTS_STEP                 = 1
POINTS_PIECE_FINISH         = 140
POINTS_PIECE_FINISHING_LANE = 10
POINTS_PIECE_AT_HOME        = -250
POINTS_INVALID_MOVE_CHOSEN  = -10


class Player:
    def __init__(self, gamemode=None):
        self.pieces = []
        playerData = PlayerData.getPlayerData()
        self.id = playerData.id

        self.startPosition = playerData.startPosition
        self.endPosition = playerData.endPosition
        self.piecesFinished = 0

        # Used for fitness score
        self.invalidMovesChosen = 0


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
            self.pieces.append(Piece.Piece(self, i))

    def hasWon(self):
        return self.piecesFinished == 4

    def piecesAtHome(self):
        count = 0
        for p in self.pieces:
            if p.atHome:
                count+=1
        return count

    def incInvalidMoveChosen(self):
        self.invalidMovesChosen += 1

    def getFitness(self):
        totalSteps = 0
        piecesFinished = 0
        stepsFinishingLane = 0
        piecesAtHome = 0
        for piece in self.pieces:
            totalSteps += min(config.MAX_STEPS, piece.stepsMoved)
            if piece.atHome:
                piecesAtHome += 1
            elif piece.hasFinished:
                piecesFinished += 1
                stepsFinishingLane += config.MAX_FINISH_LANE_POSITIONS
            elif piece.onFinishStretch:
                stepsFinishingLane += min(config.MAX_FINISH_LANE_POSITIONS, piece.pos)
        # Points for steps
        fitness  = totalSteps*POINTS_STEP
        # Points for piece finishing
        fitness += piecesFinished*POINTS_PIECE_FINISH
        # Points for steps on last stretch
        fitness += stepsFinishingLane*POINTS_PIECE_FINISHING_LANE
        # Points for pieces at home
        fitness += piecesAtHome*POINTS_PIECE_AT_HOME
        # Points for invalid moves
        # fitness += self.invalidMovesChosen*POINTS_INVALID_MOVE_CHOSEN
        return fitness

    def getStartPos(self):
        return self.startPosition

    def getEndPos(self):
        return self.endPosition

    def getId(self):
        return self.id
