import random
from collections import defaultdict

from pygame.math import Vector2

LEGAL_ACTS = ["up", "left", "down", "right"]
LEARNING_RATE = 0.5
DISCOUNT_FACTOR = 0.8
EXPLORATION_FACTOR = 0.2

class State():
    def __init__(self, apple_pos, player_body, player_score, player_dir, AI_body, AI_score, AI_dir):
        self.apple_pos = apple_pos
        self.player_body = player_body
        self.player_score = player_score
        self.player_dir = player_dir
        self.AI_body = AI_body
        self.AI_score = AI_score
        self.AI_dir = AI_dir

class Controller(object):

    def on_move(self, state, move, new_state, score):
        pass

    def get_move(self, *args, **kwargs):
        raise RuntimeError("You didn't override getmove!")

class GreedyController(Controller):

    # Initialise the new policy
    def __init__(self, policy = None):
        if not policy:
            policy = defaultdict( lambda: defaultdict( int ) )
        self.policy = policy
        self.history = []

    # Return the values of each state
    def state_value(self, state, fn = max):
        if not self.policy[state]:
            return 0
        return fn( self.policy[state].values() )

    # Return the best value for each state
    def state_value_agg(self, fn = max):
        best = None
        for state in self.policy:
            value = self.state_value(state, fn)
            if best == None or value > best:
                best = value
        return best

    # Returns the state-action policy in the Q-table
    def Q(self, state, action):
        return self.policy[state][action]

    # Returns the minimum value of the sate
    def min_state_value(self):
        value = 0
        for state in self.policy:
            value = min( value, self.state_value(state, min) )
        return value

    # Q-learning for every movement
    def on_move(self, state, action, new_state, reward):
        """When we move, update the Q-Learning table"""
        # update table
        Q = self.policy

        # Keep track of the history (for offline learning)
        # calculate features:
        # s_features = self.state_to_features(state)
        # sprime_features = self.state_to_features( new_state )
        # self.history.append( s_features + [action, reward] + sprime_features  )

        # find what the best predicted 'next reward' would have been
        max_succ = 0
        if Q[new_state]:
            max_succ = max( Q[new_state].values() )

        # update the table according to the Q-Learning equation
        Q[state][action] = Q[state][action] + LEARNING_RATE * ( reward + DISCOUNT_FACTOR * max_succ ) - Q[state][action]
        self.state = new_state

    # Selects the best move to do or explores a random move (20% chance)
    def get_move(self, state, **kwargs):
        if random.uniform(0, 1) < EXPLORATION_FACTOR:
            if(state.AI_dir == Vector2(0, -1)): # UP direction
                return random.choice(["up", "left", "right"])
            elif(state.AI_dir == Vector2(0, 1)): # DOWN direction
                return random.choice(["down", "left", "right"])
            elif(state.AI_dir == Vector2(-1, 0)): # LEFT direction
                return random.choice(["up", "down", "left"])
            elif(state.AI_dir == Vector2(1, 0)): # RIGHT direction
                return random.choice(["up", "down", "right"])
        else:
            return self.exploit(state)

    # Selects the best action regarding the action score
    def exploit(self, state):
        best_choice = None
        best_score = -10000

        if(state.AI_dir == Vector2(0, -1)): # UP direction
            legal_moves = ["up", "left", "right"]
        elif(state.AI_dir == Vector2(0, 1)): # DOWN direction
            legal_moves = ["down", "left", "right"]
        elif(state.AI_dir == Vector2(-1, 0)): # LEFT direction
            legal_moves = ["up", "down", "left"]
        elif(state.AI_dir == Vector2(1, 0)): # RIGHT direction
            legal_moves = ["up", "down", "right"]

        for action in legal_moves:
            act_score = self.policy[state][action]
            if act_score > best_score or (act_score == best_score and random.choice( [False, True] ) ):
                best_choice = action
                best_score = act_score

        return best_choice

    def next_direction(self, move, snake_dir):
        if move == "up":
            if snake_dir.y != 1:
                snake_dir = Vector2(0,-1)
        elif move == "down":
            if snake_dir.y != -1:
                snake_dir = Vector2(0,1)
        elif move == "left":
            if snake_dir.x != 1:
                snake_dir = Vector2(-1,0)
        elif move == "right":
            if snake_dir.x != -1:
                snake_dir = Vector2(1,0)
                
        return snake_dir

    def calculate_reward(self, snake_body, fruit_pos):
        if(snake_body[0] == fruit_pos):
            return 1
        else:
            return 0