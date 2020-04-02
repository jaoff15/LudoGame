import config


playerId = 0
colors = ["Green", "Yellow", "Red", "Blue"]
# startPositions = [0, 13, 26, 39]

def getPlayerData():
    global playerId
    id = playerId
    playerData = PlayerData(id, colors[id], 1 + id * 13)
    playerId += 1
    return playerData

def reset():
    global playerId
    playerId = 0


class PlayerData:
    def __init__(self, id, color, startPosition):
        self.id = id
        self.color = color
        self.startPosition = startPosition
        self.endPosition = (startPosition + config.MAX_STEPS) % config.MAX_POSITIONS
