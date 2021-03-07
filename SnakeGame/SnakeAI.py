import random

LEGAL_ACTS = ["up", "left", "down", "right"]

class SnakeAI(object):
    def __init__(self):
        self.qtable = {}
        self.learningRate = 0.1
        self.discountFactor = 0.1

    def q(self, state, action):
        if(state, action) in self.qtable:
            return self.qtable[(state, action)]
        else:
            return 0

    def on_move(self, state, move, new_state, score):
        currentValue = self.q(state, move)
        bestSuccState = 0 # Get q(new_state, bestAction)

        self.qtable[(state, move)] = currentValue + (score + self.discountFactor * bestSuccState - currentValue)

    def get_move(self, *args, **kwargs):
        return random.choice(LEGAL_ACTS)