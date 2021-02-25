import pygame
import sys

from pygame.constants import K_s
from Fruit import *
from Snake import *
from Main import *
from SnakeAI import *

pygame.mixer.pre_init(44100,-16,2,512) 
pygame.init()

cellSize = 40
cellNumber = 20
screen = pygame.display.set_mode((cellNumber*cellSize, cellNumber*cellSize))
clock = pygame.time.Clock()
mainGame = Main(cellNumber)
snakeML = SnakeAI()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 120)

# Main Loop
while True:
    # Events loop
    for event in pygame.event.get():
        if event.type == SCREEN_UPDATE:
            mainGame.update()

        # Snake input events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if mainGame.snake.direction.y != 1:
                    mainGame.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if mainGame.snake.direction.y != -1:
                    mainGame.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if mainGame.snake.direction.x != 1:
                    mainGame.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if mainGame.snake.direction.x != -1:
                    mainGame.snake.direction = Vector2(1,0)

        move = snakeML.get_move()
        if move == "up":
            if mainGame.snakeAI.direction.y != 1:
                mainGame.snakeAI.direction = Vector2(0,-1)
        elif move == "down":
            if mainGame.snakeAI.direction.y != -1:
                mainGame.snakeAI.direction = Vector2(0,1)
        elif move == "left":
            if mainGame.snakeAI.direction.x != 1:
                mainGame.snakeAI.direction = Vector2(-1,0)
        elif move == "right":
            if mainGame.snakeAI.direction.x != -1:
                mainGame.snakeAI.direction = Vector2(1,0)
        print("Snake move:", move)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit

    # Draw elements
    screen.fill((175,215,70))
    mainGame.drawElements(cellSize, screen)

    pygame.display.update()
    clock.tick(60)