import NeuralNetwork.ActivationFunctions as af
import random

def getRandomNumb():
    # Range [-1,1]
    return (2 * random.random()) - 1

class Neuron():
    def __init__(self, activationFunction, noWeights, weights=None):
        self.weights = []
        self.noWeights = noWeights
        self.bias = getRandomNumb()
        self.af = activationFunction

        if weights != None and len(weights) == noWeights:
            self.weights = weights
        else:
            for i in range(0,noWeights):
                self.weights.append(getRandomNumb())


    def ff(self, inputs):
        assert len(inputs) == self.noWeights, "Wrong input array size"
        sum = self.bias
        for i in range(0, self.noWeights):
            sum += inputs[i] * self.weights[i]
        return self.af.activate(sum)

