
import config
import random
from numba import jit

# def getNextPosNoFinish(pos, steps):
#     nextPosRaw = (pos + steps) % (config.MAX_POSITIONS + 1)
#     nextPos = 1 if nextPosRaw == 0 else nextPosRaw
#
#     assert not nextPos <= 0, "Position cannot be 0 or less"
#     assert not nextPos > config.MAX_POSITIONS, "Position cannot be more than MAX_POSITIONS"
#     return nextPos

@jit(nopython=True)
def getNextPos(pos, steps, stepsMoved = -1):
    # Will finish
    willFinish = False
    if stepsMoved is not -1:
        stepsMoved = stepsMoved + steps
        if stepsMoved > config.MAX_STEPS:
            willFinish = True
        if config.ENABLE_CHECKS:
            assert not stepsMoved > config.MAX_STEPS + 6, "Steps cannot be more than MAX_STEPS + 6"

    # Get next pos
    nextPosRaw = (pos + steps) % (config.MAX_POSITIONS + 1)
    nextPos    = 1 if nextPosRaw == 0 else nextPosRaw

    # Check data validity
    if config.ENABLE_CHECKS:
        assert not nextPos <= 0, "Position cannot be 0 or less"
        assert not nextPos > config.MAX_POSITIONS, "Position cannot be more than MAX_POSITIONS"

    return nextPos, willFinish

@jit(nopython=True)
def getPos(pos, maxPos, i):
    return (pos + i) % maxPos

class Piece:
    def __init__(self, player, id):
        self.id              = id
        self.pos             = None
        self.lastPos         = self.pos
        self.stepsMoved      = 0
        self.atHome          = True
        self.onFinishStretch = False
        self.hasFinished     = False
        self.player          = player

        self.behind     = [0] * 12
        self.infront    = [0] * 12

    def updateSurroundings(self, players):
        if not self.atHome and not self.onFinishStretch and not self.hasFinished:
            enemies = []
            for player in players:
                for piece in player.pieces:
                    if not piece.atHome and not piece.hasFinished and not piece.onFinishStretch:
                        enemies.append(piece.pos)

            for i in range(1, 13):
                # self.infront[i - 1] = 1 if (self.pos + i) % config.MAX_POSITIONS in enemies else 0
                # self.behind[i - 1]  = 1 if (self.pos - i) % config.MAX_POSITIONS in enemies else 0
                self.infront[i - 1] = 1 if getPos(self.pos,config.MAX_POSITIONS,i) in enemies else 0
                self.behind[i - 1]  = 1 if getPos(self.pos,config.MAX_POSITIONS,-i) in enemies else 0

    def move(self, steps):

        if self.onFinishStretch:
            # Finishing
            self.lastPos = self.pos

            nextPos = self.pos + steps
            if nextPos > config.MAX_FINISH_LANE_POSITIONS:
                nextPos2 = config.MAX_FINISH_LANE_POSITIONS - (nextPos - config.MAX_FINISH_LANE_POSITIONS)
                nextPos = nextPos2
            if nextPos <= 0:
                assert False, "error"
            self.pos = nextPos

            if config.ENABLE_CHECKS:
                assert not self.pos <= 0, "Position cannot be 0 or less"
                assert not self.pos > config.MAX_FINISH_LANE_POSITIONS, "Position cannot be more than MAX_POSITIONS"

            if self.pos == config.MAX_FINISH_LANE_POSITIONS:
                self.hasFinished = True
                self.player.piecesFinished += 1

                if config.PRINT_EVENTS:
                    print("Piece %s from player %s finished from pos %s to pos %s on the finishing lane with %s steps" % (
                        self.id, self.player.id, self.lastPos, self.pos, steps))
                elif config.PRINT_PIECE_FINISHES:
                    print(
                        "Piece %s from player %s finished" % (self.id, self.player.id))
            else:
                if config.PRINT_EVENTS:
                    print("Piece %s from player %s moved from pos %s to pos %s on the finishing lane with %s steps" % (
                        self.id, self.player.id, self.lastPos, self.pos, steps))

        else:
            # Out on board
            self.lastPos = self.pos
            self.stepsMoved += steps
            if self.stepsMoved > config.MAX_STEPS:
                self.onFinishStretch = True
                self.pos = self.stepsMoved % (config.MAX_STEPS + 1)

                if config.PRINT_EVENTS:
                    print("Moved piece %s from player %s from pos %s to pos %s on the finishing lane with %s steps" % (self.id, self.player.id, self.lastPos,self.pos, steps))
            else:
                # nextPos = (self.pos + steps) % (config.MAX_POSITIONS+1)
                # self.pos = 1 if nextPos == 0 else nextPos

                [self.pos, _] = getNextPos(self.pos, steps)

                if config.PRINT_EVENTS:
                    print("Moved piece %s from player %s from pos %s to pos %s with %s steps" % (self.id, self.player.id, self.lastPos,self.pos, steps))



    def moveOutOnBoard(self, d):
        self.lastPos = self.pos
        self.atHome = False
        self.onFinishStretch = False
        self.stepsMoved = 0
        self.pos = self.player.getStartPos()
        if config.PRINT_EVENTS:
            print("Moved piece %s from player %s out from home with dice throw %s" % (self.id, self.player.id, d))
        elif config.PRINT_PIECES_MOVED_FROM_HOME:
            print("Moved piece %s from player %s out from home" % (self.id, self.player.id))

    def moveHome(self):
        self.lastPos    = 0
        self.atHome     = True
        self.pos        = None
        self.stepsMoved = 0
        self.onFinishStretch = False
        if config.PRINT_EVENTS == True or config.PRINT_PIECE_KNOCKED_HOME == True:
            print("Moved piece %s from player %s home" % (self.id, self.player.id))


    def willHitGoal(self, dice):
        if self.atHome or self.hasFinished or not self.onFinishStretch:
            return False
        if self.pos + dice == config.MAX_FINISH_LANE_POSITIONS:
            return True
        return False

    def willKnockHomeEnemy(self, dice, otherPlayers):
        # Home or on finishing stretch
        if self.atHome or self.hasFinished or self.onFinishStretch:
            return False
        # Will move into finishing stretch
        if self.pos + dice > config.MAX_STEPS:
            return False
        newPos = self.pos + dice
        for player in otherPlayers:
            for piece in player.pieces:
                if newPos == piece.pos:
                    return True
        return False

    # def _getEnemyCount(self, pos, otherPlayers, inFront):
    #     count = 0
    #     zone = [None] * 6
    #     for i in range(1, 7):
    #         if inFront:
    #             zone[i-1] = (pos + i) % config.MAX_POSITIONS
    #         else:
    #             zone[i-1] = (pos - i) % config.MAX_POSITIONS
    #     for player in otherPlayers:
    #         for piece in player.pieces:
    #             if piece.pos in zone:
    #                 count += 1
    #     return count

    def willMoveToLessDangerousPos(self, dice):
        # Home or on finishing stretch
        if self.atHome or self.hasFinished or self.onFinishStretch:
            return False
        # Will move into finishing stretch
        if self.pos + dice > config.MAX_STEPS:
            return True

        # Get enemy counts
        currentEnemyCount = sum(self.behind[0:6])
        newEnemyCount = sum(self.behind[dice:dice + 6])
        return newEnemyCount < currentEnemyCount

        # currentDangerLevel = self._getEnemyCount(self.pos, otherPlayers, False)
        # Find new danger level
        # newPos = (self.pos + dice) % config.MAX_POSITIONS
        # newDangerLevel = self._getEnemyCount(newPos, otherPlayers, False)
        # return newDangerLevel < currentDangerLevel

    def willMoveWithinKnockingDistance(self, dice):
        # Home or on finishing stretch
        if self.atHome or self.hasFinished or self.onFinishStretch:
            return False
        # Will move into finishing stretch
        if self.pos + dice > config.MAX_STEPS:
            return False
        # Count enemies in front and if its over 0 there is possibility of knocking home
        # currentEnemyCount = sum(self.behind[dice:dice+6])
        # return self._getEnemyCount(self.pos, otherPlayers, True) > 0

        return  sum(self.infront[dice:dice+6]) > 0

    def willMoveToMoreDangerousPos(self, dice):
        # Home or on finishing stretch
        if self.atHome or self.hasFinished or self.onFinishStretch:
            return False
        # Will move into finishing stretch
        if self.pos + dice > config.MAX_STEPS:
            return False
        # Find current danger level
        currentEnemyCount = sum(self.behind[0:6])
        newEnemyCount = sum(self.behind[dice:dice + 6])
        return newEnemyCount > currentEnemyCount

        # currentDangerLevel = self._getEnemyCount(self.pos, otherPlayers, False)
        # Find new danger level
        # newPos = (self.pos + dice) % config.MAX_POSITIONS
        # newDangerLevel = self._getEnemyCount(newPos, otherPlayers, False)
        # return newDangerLevel > currentDangerLevel

    def willBounceOffGoal(self, dice):
        if self.atHome or self.hasFinished or not self.onFinishStretch:
            return False
        if self.pos + dice == config.MAX_FINISH_LANE_POSITIONS:
            return False
        return True

def selectRandomMove(availableMoves):
    if len(availableMoves) > 0:
        m = random.randint(0, len(availableMoves)-1)
        return availableMoves[m]
    else:
        return "MovePiece" + str(random.randint(1, 4))