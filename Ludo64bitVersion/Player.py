
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
        self.pieces = []
        playerData = PlayerData.getPlayerData()
        self.id = playerData.id
        self.color = playerData.color
        self.startPosition = playerData.startPosition
        self.endPosition = playerData.endPosition
        self.piecesFinished = 0

        self.invalidMovesChosen = 0

        # Fitness
        # self.fitness = 0
        # self.timesKnockedHome = 0
        # self.timesKnockedOtherHome = 0
        # self.timesChosenInvalidMoves = 0
        # self.timesChosenValidMoves = 0
        #
        # self.decay        = 1
        # self.decayPerTurn = 0.005


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
        # for piece in self.pieces:
        #     if not piece.hasFinished:
        #         return False
        # return True

    def incInvalidMoveChosen(self):
        self.invalidMovesChosen += 1

    # def getInvalidMoveCount(self):
    #     return self.invalidMovesChosen

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

        fitness  = totalSteps*POINTS_STEP                           # Points for steps
        fitness += piecesFinished*POINTS_PIECE_FINISH               # Points for piece finishing
        fitness += stepsFinishingLane*POINTS_PIECE_FINISHING_LANE   # Points for steps on last stretch
        fitness += piecesAtHome*POINTS_PIECE_AT_HOME                # Points for pieces at home
        fitness += self.invalidMovesChosen*POINTS_INVALID_MOVE_CHOSEN
        return fitness

    def getStartPos(self):
        return self.startPosition

    def getEndPos(self):
        return self.endPosition

    def getId(self):
        return self.id

    def getColor(self):
        return self.color
