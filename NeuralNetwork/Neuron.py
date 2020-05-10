import NeuralNetwork.ActivationFunctions as af
import random

def getRandomNumb():
    # Range [-1,1]
    return (2 * random.random()) - 1

class Neuron():
    def __init__(self, activationFunction, noWeights, weights=None, biasWeight = None):
        self.weights = []
        self.noWeights = noWeights
        self.af = activationFunction

        if biasWeight is None:
            self.bias = getRandomNumb()
        else:
            self.bias = biasWeight


        if weights != None and len(weights) == noWeights:
            self.weights = weights
        else:
            for i in range(0,noWeights):
                self.weights.append(getRandomNumb())


    def ff(self, inputs):
        assert len(inputs) == self.noWeights, "Wrong input array size"
        assert type(self.bias) is not 'float', "Bias should be a float"
        sum = self.bias
        for i in range(0, self.noWeights):
            # if type(inputs)=='list':
            sum += inputs[i] * self.weights[i]
            # else:
            #     sum += inputs[0] * self.weights[0]
        return self.af.activate(sum)

