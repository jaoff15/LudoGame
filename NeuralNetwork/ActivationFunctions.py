
import math


clamp = lambda n, minn, maxn: max(min(maxn, n), minn)

class Logistic:
    def activate(self, input):
        # input = clamp(input, 100, -100)
        return 1.0 / (1.0 + math.exp(-input))


    def derivedActivate(self, input):
        # input = clamp(input, 100, -100)
        return input * (1.0 - input)



class Tanh:
    def activate(self, input):
        return 2.0 / (1.0 + math.pow(math.e, -2.0*input)) - 1.0

    def derivedActivate(self, input):
        return 1.0-(input*input)

class NoActivationFunction:
    def activate(self, input):
        return input

    def derivedActivate(self, input):
        return input