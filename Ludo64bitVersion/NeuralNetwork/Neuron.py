import NeuralNetwork.ActivationFunctions as af
import random
import config

def getRandomNumb():
    # Range [-1,1]
    return (2 * random.random()) - 1

class Neuron():
    def __init__(self, activationFunction, noWeights, weights=None, biasWeight = None):
        # Activation Function
        self.af = activationFunction

        # Bias
        if biasWeight is None:
            self.bias = getRandomNumb()
        else:
            self.bias = biasWeight

        # Weights
        self.weights = []
        self.noWeights = noWeights
        if weights != None and len(weights) == noWeights:
            self.weights = weights
        else:
            for i in range(0,noWeights):
                self.weights.append(getRandomNumb())


    def ff(self, inputs):
        if config.ENABLE_CHECKS:
            assert len(inputs) == self.noWeights, "Wrong input array size"
            assert type(self.bias) is not 'float', "Bias should be a float"
        sum = self.bias
        for i in range(0, self.noWeights):
            sum += inputs[i] * self.weights[i]
        return self.af.activate(sum)

