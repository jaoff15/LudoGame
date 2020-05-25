import random
import config
from numba import jit
import numpy as np

@jit(nopython=True)
def getRandomNumb():
    # Range [-1,1]
    return (2 * random.random()) - 1

class Neuron():
    def __init__(self, activationFunction, noWeights, weights=[], biasWeight = None):
        # Activation Function
        self.af = activationFunction

        # Bias
        self.bias = getRandomNumb() if  biasWeight == None else biasWeight

        # Weights
        self.weights = np.zeros(noWeights)
        self.noWeights = noWeights

        assert len(weights) == noWeights or len(weights) == 0, "Weight array has the wrong length"

        if len(weights) == noWeights:
            self.weights = np.array(weights)
        else:

            for i in range(0,noWeights):
                self.weights[i] = getRandomNumb()

    def ff(self, inputs):
        if config.ENABLE_CHECKS:
            assert len(inputs) == self.noWeights, "Wrong input array size"
            assert type(self.bias) is not 'float', "Bias should be a float"

        if len(self.weights) == 1:
            sum = np.dot(inputs, self.weights)
        else:
            sum = matrixMult(inputs, self.weights)
        return self.af.activate(sum+self.bias)


@jit(nopython=True)
def matrixMult(inputs,  weights):
    return np.dot(inputs, weights)
