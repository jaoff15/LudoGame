

# General for game play
MAX_STEPS                   = 50
MAX_POSITIONS               = 52
MAX_PLAYERS                 = 4
MAX_PIECES                  = 4
MAX_FINISH_LANE_POSITIONS   = 6

# Print configuration
PRINT_EVENTS                 = False
PRINT_PIECE_FINISHES         = False
PRINT_PIECES_MOVED_FROM_HOME = False
PRINT_PIECE_KNOCKED_HOME     = False
PRINT_WINNER                 = False
PRINT_NO_MOVE                = False
PRINT_FITNESS_SCORES         = False
PRINT_BEST_FITNESS_SCORE     = True
PRINT_PLAYER_WINS            = True
PRINT_ROUNDS_PLAYED          = False
PRINT_EXECUTION_TIME         = True
PRINT_FF_TIME                = False
ENABLE_CHECKS                = True


# AI controller parameters
INDIVIDUALS_PER_PLAYER = 100    # Number of neural network individuals per ludo player
NO_ELITE_CARRYOVER = 50         # Number of the best individuals from previous game being carried over to next game
AMOUNT_OF_MUTATION = 1          # [%] Chance of a parameter experiencing mutation
NO_GAMES_BETWEEN_PERFORMANCE_TEST = 100
