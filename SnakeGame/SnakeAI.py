import random

LEGAL_ACTS = ["up", "left", "down", "right"]

class SnakeAI(object):
    def on_move(self, state, move, new_state, score):
        pass

    def get_move(self, *args, **kwargs):
        return random.choice(LEGAL_ACTS)