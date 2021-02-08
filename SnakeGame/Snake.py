import pygame
from pygame.math import Vector2

class Snake:

    def __init__(self, enemy):        
        self.newBlock = False
        self.enemy = enemy
        self.score = 0

        if not self.enemy:
            self.body = [Vector2(4,9), Vector2(3,9), Vector2(2,9)]
            self.direction = Vector2(1,0)

            self.headUp = pygame.image.load('Graphics/head_up.png').convert_alpha()
            self.headDown = pygame.image.load('Graphics/head_down.png').convert_alpha()
            self.headRight = pygame.image.load('Graphics/head_right.png').convert_alpha()
            self.headLeft = pygame.image.load('Graphics/head_left.png').convert_alpha()
            self.tailUp = pygame.image.load('Graphics/tail_up.png').convert_alpha()
            self.tailDown = pygame.image.load('Graphics/tail_down.png').convert_alpha()
            self.tailRight = pygame.image.load('Graphics/tail_right.png').convert_alpha()
            self.tailLeft = pygame.image.load('Graphics/tail_left.png').convert_alpha()
            self.bodyVertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
            self.bodyHorizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
            self.bodyTR = pygame.image.load('Graphics/body_tr.png').convert_alpha()
            self.bodyTL = pygame.image.load('Graphics/body_tl.png').convert_alpha()
            self.bodyBR = pygame.image.load('Graphics/body_br.png').convert_alpha()
            self.bodyBL = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        else:
            self.body = [Vector2(15,11), Vector2(16,11), Vector2(17,11)]
            self.direction = Vector2(-1,0)

            self.headUp = pygame.image.load('Graphics/head_up-AI.png').convert_alpha()
            self.headDown = pygame.image.load('Graphics/head_down-AI.png').convert_alpha()
            self.headRight = pygame.image.load('Graphics/head_right-AI.png').convert_alpha()
            self.headLeft = pygame.image.load('Graphics/head_left-AI.png').convert_alpha()
            self.tailUp = pygame.image.load('Graphics/tail_up-AI.png').convert_alpha()
            self.tailDown = pygame.image.load('Graphics/tail_down-AI.png').convert_alpha()
            self.tailRight = pygame.image.load('Graphics/tail_right-AI.png').convert_alpha()
            self.tailLeft = pygame.image.load('Graphics/tail_left-AI.png').convert_alpha()
            self.bodyVertical = pygame.image.load('Graphics/body_vertical-AI.png').convert_alpha()
            self.bodyHorizontal = pygame.image.load('Graphics/body_horizontal-AI.png').convert_alpha()
            self.bodyTR = pygame.image.load('Graphics/body_tr-AI.png').convert_alpha()
            self.bodyTL = pygame.image.load('Graphics/body_tl-AI.png').convert_alpha()
            self.bodyBR = pygame.image.load('Graphics/body_br-AI.png').convert_alpha()
            self.bodyBL = pygame.image.load('Graphics/body_bl-AI.png').convert_alpha()

        self.crunchSound = pygame.mixer.Sound('Sound/crunch.wav')

    def drawSnake(self, cellSize, screen):
        self.updateHeadGraphics()
        self.updateTailGraphics()

        for index, block in enumerate(self.body):
            # 1. Needs a rect for the positioning
            xPos = int(block.x * cellSize)
            yPos = int(block.y * cellSize)
            blockRect = pygame.Rect(xPos, yPos, cellSize, cellSize)

            if index == 0: # What direction is the face heading
                screen.blit(self.head, blockRect)
            elif index == len(self.body) - 1: # What direction is the tail facing
                screen.blit(self.tail, blockRect)
            else:
                self.previousBlock = self.body[index + 1] - block
                self.nextBlock = self.body[index - 1] - block

                if self.previousBlock.x == self.nextBlock.x: # Snake is moving vertical
                    screen.blit(self.bodyVertical, blockRect)
                if self.previousBlock.y == self.nextBlock.y: # Snake is moving horizontal
                    screen.blit(self.bodyHorizontal, blockRect)
                else: # Snake is turning
                    if self.previousBlock.x == -1 and self.nextBlock.y == -1 or self.previousBlock.y == -1 and self.nextBlock.x == -1: # Top-left turn
                        screen.blit(self.bodyTL, blockRect)
                    if self.previousBlock.x == -1 and self.nextBlock.y == 1 or self.previousBlock.y == 1 and self.nextBlock.x == -1: # Bottom-left turn
                        screen.blit(self.bodyBL, blockRect)
                    if self.previousBlock.x == 1 and self.nextBlock.y == -1 or self.previousBlock.y == -1 and self.nextBlock.x == 1: # Top-right turn
                        screen.blit(self.bodyTR, blockRect)
                    if self.previousBlock.x == 1 and self.nextBlock.y == 1 or self.previousBlock.y == 1 and self.nextBlock.x == 1: # Bottom-right turn
                        screen.blit(self.bodyBR, blockRect)

    def updateHeadGraphics(self):
        headDirection = self.body[1] - self.body[0]

        if headDirection == Vector2(1,0):
            self.head = self.headLeft
        if headDirection == Vector2(-1,0):
            self.head = self.headRight
        if headDirection == Vector2(0,1):
            self.head = self.headUp
        if headDirection == Vector2(0,-1):
            self.head = self.headDown

    def updateTailGraphics(self):
        tailDirection = self.body[-2] - self.body[-1]

        if tailDirection == Vector2(1,0):
            self.tail = self.tailLeft
        if tailDirection == Vector2(-1,0):
            self.tail = self.tailRight
        if tailDirection == Vector2(0,1):
            self.tail = self.tailUp
        if tailDirection == Vector2(0,-1):
            self.tail = self.tailDown

    def moveSnake(self):
        if self.newBlock:
            bodyCopy = self.body[:]
            bodyCopy.insert(0, bodyCopy[0] + self.direction)
            self.body = bodyCopy[:]
            self.newBlock = False
        else:
            bodyCopy = self.body[:-1]
            bodyCopy.insert(0, bodyCopy[0] + self.direction)
            self.body = bodyCopy[:]

    def addBlock(self):
        self.newBlock = True

    def playCrunchSound(self):
        self.crunchSound.play()

    def reset(self):
        if not self.enemy:
            self.body = [Vector2(5,9), Vector2(4,9), Vector2(3,9)]
            self.direction = Vector2(1,0)
            self.score = 0
        else:
            self.body = [Vector2(15,11), Vector2(16,11), Vector2(17,11)]
            self.direction = Vector2(-1,0)
            self.score = 0