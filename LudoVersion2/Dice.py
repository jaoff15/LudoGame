import random
import numpy as np
from numba import jit

# def generateDiceThrows(maxRounds):
#     # return __normal(maxRounds)
#     # return __normalWithSixes(maxRounds)
#     return __higherThrowPropability(maxRounds)


# @jit(nopython=True)
def roll():
    # return random.randint(1, 6)
    return (random.choices([1 ,2 ,3 ,4 ,5 ,6] ,[1 ,2 ,3 ,4 ,5 ,6]))[0]

# # Version 1 - Random
# def __normal(maxRounds):
#     diceThrows = []
#     for i in range(0, maxRounds):
#         diceThrows.append(random.randint(1, 6))
#     return diceThrows
#
# # Version 2 - Random but at least one 6
# def __normalWithSixes(maxRounds):
#     diceThrows = []
#     while 6 not in diceThrows:
#         diceThrows = []
#         for i in range(0,maxRounds):
#             diceThrows.append(random.randint(1,6))
#     return diceThrows
#
# # Version 3 - Make a higher proportion 6's
# def __higherThrowPropability(maxRounds):
#     diceThrows = np.zeros(maxRounds)
#     for i in range(0, maxRounds):
#         diceThrows[i] = ((random.choices([1 ,2 ,3 ,4 ,5 ,6] ,[1 ,2 ,3 ,4 ,5 ,6]))[0])
#     return diceThrows