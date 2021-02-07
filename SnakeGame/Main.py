from Snake import *
from Fruit import *
from pygame.math import Vector2

class Main:

    def __init__(self, cellNumber):
        self.gameFont = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
        self.apple = pygame.image.load('Graphics/apple.png').convert_alpha()
        self.cellNumber = cellNumber
        self.snake = Snake(False)
        self.snakeAI = Snake(True)
        self.fruit = Fruit(cellNumber)

    def update(self):
        self.snake.moveSnake()
        self.snakeAI.moveSnake()
        self.checkCollision()
        self.checkFail()

    def drawElements(self, cellSize, screen):
        self.drawGrass(cellSize, screen)
        self.snake.drawSnake(cellSize, screen)
        self.snakeAI.drawSnake(cellSize, screen)
        self.fruit.drawFruit(cellSize, screen)
        self.drawScore(screen, cellSize)

    def checkCollision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomFruit()
            self.snake.addBlock()
            self.snake.playCrunchSound()

        if self.fruit.pos == self.snakeAI.body[0]:
            self.fruit.randomFruit()
            self.snakeAI.addBlock()
            self.snakeAI.playCrunchSound()
        
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomFruit()

    def checkFail(self):
        # Check if the snake gets out of the screen
        if self.snake.body[0].x < 0:
            self.snake.body[0].x = self.cellNumber
        if self.snake.body[0].x > self.cellNumber:
            self.snake.body[0].x = 0
        if self.snake.body[0].y < 0:
            self.snake.body[0].y = self.cellNumber
        if self.snake.body[0].y > self.cellNumber:
            self.snake.body[0].y = 0

        if self.snakeAI.body[0].x < 0:
            self.snakeAI.body[0].x = self.cellNumber
        if self.snakeAI.body[0].x > self.cellNumber:
            self.snakeAI.body[0].x = 0
        if self.snakeAI.body[0].y < 0:
            self.snakeAI.body[0].y = self.cellNumber
        if self.snakeAI.body[0].y > self.cellNumber:
            self.snakeAI.body[0].y = 0

        # Check if the snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()

        for block in self.snakeAI.body[1:]:
            if block == self.snakeAI.body[0]:
                self.gameOver()

    def gameOver(self):
        self.snake.reset()
        self.snakeAI.reset()

    def drawGrass(self, cellSize, screen):
        grassColor = (167,209,61)

        for row in range(self.cellNumber):
            if row % 2 == 0:
                for col in range(self.cellNumber):
                    if col % 2 == 0:
                        grassRect = pygame.Rect(col * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grassColor, grassRect)
            else:
                for col in range(self.cellNumber):
                    if col % 2 != 0:
                        grassRect = pygame.Rect(col * cellSize, row * cellSize, cellSize, cellSize)
                        pygame.draw.rect(screen, grassColor, grassRect)

    def drawScore(self, screen, cellSize):
        # RED score
        scoreText = str(len(self.snakeAI.body) - 3)
        scoreSurface = self.gameFont.render(scoreText, True, (56,74,12))
        scorePosition = Vector2(int(cellSize * self.cellNumber - 60), int(cellSize * self.cellNumber - 40))
        scoreRect = scoreSurface.get_rect(center = (scorePosition.x, scorePosition.y))
        appleRect = self.apple.get_rect(midright = (scoreRect.left, scoreRect.centery))
        bgRect = pygame.Rect(appleRect.left, appleRect.top, appleRect.width + scoreRect.width + 6, appleRect.height)

        pygame.draw.rect(screen, (167,209,61), bgRect)
        pygame.draw.rect(screen, (255,92,58), bgRect, 2)
        screen.blit(scoreSurface, scoreRect)
        screen.blit(self.apple, appleRect)

        # BLUE score
        scoreText = str(len(self.snake.body) - 3)
        scoreSurface = self.gameFont.render(scoreText, True, (56,74,12))
        scorePosition = Vector2(94, int(cellSize * self.cellNumber - 40))
        scoreRect = scoreSurface.get_rect(center = (scorePosition.x, scorePosition.y))
        appleRect = self.apple.get_rect(midright = (scoreRect.left, scoreRect.centery))
        bgRect = pygame.Rect(appleRect.left, appleRect.top, appleRect.width + scoreRect.width + 6, appleRect.height)

        pygame.draw.rect(screen, (167,209,61), bgRect)
        pygame.draw.rect(screen, (83,148,250), bgRect, 2)
        screen.blit(scoreSurface, scoreRect)
        screen.blit(self.apple, appleRect)