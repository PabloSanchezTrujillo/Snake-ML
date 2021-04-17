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

class ApproxController(Controller):

    def __init__(self, weights):
        self.weights = weights
        self.legalActs = []
        self.history = []

    def Q(self, state, action):
        features = self.getFeatures(state, action)

        if self.weights == None:
            self.weights = [ 0 ] * len(features)

        total = 0
        iteration = 0
        for j in range(0, len(features)):
            total += self.weights[j] * features[j]
        #print("Total: ", total)
        return total

    def QPrime(self, new_state):
        """Get best reward from a successor state"""

        bestValue = None
        for action in self.legalActs:
            value = self.Q(new_state, action)
            if bestValue == None or bestValue < value:
                bestValue = value
        return bestValue

    def getFeatures(self, state, action):
        """Convert a state-action pair into features"""
        if action == "up":
            next_x = state.AI_body[0].x + 0
            next_y = state.AI_body[0].y - 1
        elif action == "down":
            next_x = state.AI_body[0].x + 0
            next_y = state.AI_body[0].y + 1
        elif action == "left":
            next_x = state.AI_body[0].x - 1
            next_y = state.AI_body[1].y + 0
        elif action == "right":
            next_x = state.AI_body[0].x + 1
            next_y = state.AI_body[0].y + 0

        features = []

        # Manhattan distance between the next space and some waypoints 
        #           (current apple position, current player's head, current player's tail, current AI's tail)
        score_difference = state.AI_score - state.player_score 
        waypoints = [state.apple_pos, state.player_body[0], state.player_body[-2], state.AI_body[-2]] #player_body[-2], length_difference
        for (x,y) in waypoints:
            dist_x = abs(next_x - x)
            dist_y = abs(next_y - y)
            features += [ dist_x, dist_y ]

        if len(state.AI_body) < 6:
            features[-1] = 0
            features[-2] = 0

        #print(features)

        return features

    def on_move(self, state, action, new_state, reward):
        """When we move, store the value in the history"""

        # update the weights
        self.update( state, action, reward, new_state )

        # update the current state
        self.state = new_state


    def update(self, s, action, reward, s_prime, discountFactor=0.8, learningRate=0.001):
        """Adjust the weights to adapt to observations"""
        
        # 1. get the features for the starting state
        f = self.getFeatures(s, action)

        # 2. find the best next action from the successor state according to Q:
        max_successor = self.QPrime(s_prime)
        target = reward + discountFactor * max_successor
        error = target - self.Q( s, action ) 
        #print("Error: ", error)

        # 3. calculate the error for each feature
        errors = []
        for j in range(0, len(self.weights) ):
            errors.append( learningRate * f[j] * error )

        # 4. update the weights
        for i in range( 0, len(self.weights) ):
            self.weights[i] = self.weights[i] + errors[i]

    def get_move(self, state, **kwargs):
        """Actual policy for making moves"""
        if random.uniform(0, 1) < EXPLORATION_FACTOR:
            if(state.AI_dir == Vector2(0, -1)): # UP direction
                self.legalActs = ["up", "left", "right"]
                return random.choice(["up", "left", "right"])
            elif(state.AI_dir == Vector2(0, 1)): # DOWN direction
                self.legalActs = ["down", "left", "right"]
                return random.choice(["down", "left", "right"])
            elif(state.AI_dir == Vector2(-1, 0)): # LEFT direction
                self.legalActs = ["up", "down", "left"]
                return random.choice(["up", "down", "left"])
            elif(state.AI_dir == Vector2(1, 0)): # RIGHT direction
                self.legalActs = ["up", "down", "right"]
                return random.choice(["up", "down", "right"])
        else:
            return self.exploit( state )

    def exploit(self, state):
        """Choose best based on Q values"""
        best = (None, None)

        if(state.AI_dir == Vector2(0, -1)): # UP direction
            legal_moves = ["up", "left", "right"]
        elif(state.AI_dir == Vector2(0, 1)): # DOWN direction
            legal_moves = ["down", "left", "right"]
        elif(state.AI_dir == Vector2(-1, 0)): # LEFT direction
            legal_moves = ["up", "down", "left"]
        elif(state.AI_dir == Vector2(1, 0)): # RIGHT direction
            legal_moves = ["up", "down", "right"]
        
        self.legalActs = legal_moves

        for action in legal_moves:
            score = self.Q( state, action )
            if best[0] is None or score > best[1]: 
                best = ( action, score )

        print(self.weights)

        return best[0]

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

    def calculate_reward(self, snake_bodyAI, snake_bodyPlayer, fruit_pos):
        # Player hits snake_AI's body
        for block in snake_bodyAI[1:]:
            if block == snake_bodyPlayer[0]:
                return 20

        # Snake_AI's head hits player's body
        for block in snake_bodyPlayer:
            if Vector2.distance_to(snake_bodyAI[0], block) <= 3:
                return -100

        # Snake_AI's head hits itself
        for block in snake_bodyAI[1:]:
            if block == snake_bodyAI[0]:
                return -100

        # Snake's head on apple position
        if(Vector2.distance_to(snake_bodyAI[0], fruit_pos) == 0):
            return 10
        # Empty square
        else:
            return 1