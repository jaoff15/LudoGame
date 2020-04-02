
import Piece
import PlayerData
import config

class Player:
    def __init__(self):
        self.pieces = []
        playerData = PlayerData.getPlayerData()
        self.id = playerData.id
        self.color = playerData.color
        self.startPosition = playerData.startPosition
        self.endPosition = playerData.endPosition

        # gamemodes
        # None : Not configured. Will give an error
        # RA   : Random player. Move will be randomly selected from the available moves.
        # MA   : Manual Player. Moved will come from the user through the MLudoPlayer class
        # SA   : Simple Automated Player. Moves will be determined by the SALudoPlayer Class
        # NN   : Neural Network Player. Moved will be determined by the NNLudoPlayer class

        self.gamemode = None

        self.__initializePlayer()

    def __initializePlayer(self):
        for i in range(1, config.MAX_PIECES+1):
            self.pieces.append(Piece.Piece(self, i))

    def getStartPos(self):
        return self.startPosition

    def getEndPos(self):
        return self.endPosition

    def getId(self):
        return self.id

    def getColor(self):
        return self.color

