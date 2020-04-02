# Possible learning rewards:
# +50 for moving piece out from home
# -50 for piece to be knocked back home
# +1 (per position) for moving piece forward
# +5 (per position) for moving piece forward in finishing lane
# -5 (per position) for moving piece backwards in finishing lane
# +100 for finishing with a piece
# Max score for perfect round:
# 50 points * 4 pieces + 52 positions * 1 point * 4 pieces + 6 positions * 5 points * 4 pieces + 100points * 4 pieces =
# Total = 928 points

rewardDefinitions = {"MovePieceOutFromHome": 50, "PieceKnockedHome": -50, "PieceMovedForward": 1,
                     "PieceMovedForwardInFinishingLane": 1,
                     "PieceMovedBackwardsInFinishingLane": -5, "PieceFinish": 100}


# This player gets it moves from a neural network
class NNLudoPlayer:
    def __init__(self):
        pass
