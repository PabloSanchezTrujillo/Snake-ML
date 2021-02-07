import pygame
import random
from pygame.math import Vector2

class Fruit:

    def __init__(self, cellNumber):        
        self.cellNumber = cellNumber
        self.randomFruit()
        self.apple = pygame.image.load('Graphics/apple.png').convert_alpha()

    def drawFruit(self, cellSize, screen):
        fruitRect = pygame.Rect(int(self.pos.x * cellSize), int(self.pos.y * cellSize), cellSize, cellSize)
        screen.blit(self.apple, fruitRect)
        #pygame.draw.rect(screen, (126,166,114), fruitRect)

    def randomFruit(self):
        self.x = random.randint(0, self.cellNumber - 1)
        self.y = random.randint(0, self.cellNumber - 1)
        self.pos = Vector2(self.x, self.y)