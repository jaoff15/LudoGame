
import config
import random

# def getNextPosNoFinish(pos, steps):
#     nextPosRaw = (pos + steps) % (config.MAX_POSITIONS + 1)
#     nextPos = 1 if nextPosRaw == 0 else nextPosRaw
#
#     assert not nextPos <= 0, "Position cannot be 0 or less"
#     assert not nextPos > config.MAX_POSITIONS, "Position cannot be more than MAX_POSITIONS"
#     return nextPos

def getNextPos(pos, steps, stepsMoved = None):
    # Will finish
    willFinish = False
    if stepsMoved is not None:
        stepsMoved += steps
        if stepsMoved > config.MAX_STEPS:
            willFinish = True
        if config.ENABLE_CHECKS:
            assert not stepsMoved > config.MAX_STEPS + 6, "Steps cannot be more than MAX_STEPS + 6"

    # Get next pos
    nextPosRaw = (pos + steps) % (config.MAX_POSITIONS + 1)
    nextPos = 1 if nextPosRaw == 0 else nextPosRaw

    # Check data validity
    if config.ENABLE_CHECKS:
        assert not nextPos <= 0, "Position cannot be 0 or less"
        assert not nextPos > config.MAX_POSITIONS, "Position cannot be more than MAX_POSITIONS"



    return nextPos, willFinish

class Piece:
    def __init__(self, player, id):
        self.id = id
        self.pos = None
        self.lastPos = self.pos
        self.stepsMoved = 0
        self.atHome = True
        self.onFinishStretch = False
        self.hasFinished = False
        self.player = player

    def move(self, steps):

        if self.onFinishStretch:
            self.lastPos = self.pos

            nextPos = self.pos + steps
            if nextPos > config.MAX_FINISH_LANE_POSITIONS:
                nextPos2 = config.MAX_FINISH_LANE_POSITIONS - (nextPos - config.MAX_FINISH_LANE_POSITIONS)
                nextPos = nextPos2
            if nextPos <= 0:
                print(" ")
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
        self.lastPos = 0
        self.atHome = True
        self.onFinishStretch = False
        self.pos = None
        self.stepsMoved = 0
        if config.PRINT_EVENTS == True or config.PRINT_PIECE_KNOCKED_HOME == True:
            print("Moved piece %s from player %s home" % (self.id, self.player.id))


def selectRandomMove(availableMoves):
    if len(availableMoves) > 0:
        m = random.randint(0, len(availableMoves)-1)
        return availableMoves[m]
    else:
        return "MovePiece" + str(random.randint(1, 4))