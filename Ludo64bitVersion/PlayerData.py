import config


playerId = 0

def getPlayerData():
    global playerId
    id = playerId
    playerData = PlayerData(id, 1 + id * 13)
    playerId += 1
    return playerData

def reset():
    global playerId
    playerId = 0


class PlayerData:
    def __init__(self, id, startPosition):
        self.id = id
        self.startPosition = startPosition
        self.endPosition = (startPosition + config.MAX_STEPS) % config.MAX_POSITIONS
