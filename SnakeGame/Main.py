from Snake import *
from Fruit import *
from SnakeAI import State
from pygame.math import Vector2

class Main:

    def __init__(self, cellNumber):
        self.gameFont = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
        self.gameFontLarge = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 120)
        self.gameFontMedium = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 60)
        self.gameFontSmall = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
        self.apple = pygame.image.load('Graphics/apple.png').convert_alpha()
        self.cellNumber = cellNumber
        self.snake = Snake(False)
        self.snakeAI = Snake(True)
        self.fruit = Fruit(cellNumber)
        self.isGameOver = False

    def currentState(self):
        return State(self.fruit.pos, self.snake.body, self.snake.score, self.snake.direction,
                        self.snakeAI.body, self.snakeAI.score, self.snakeAI.direction)

    def update(self):
        if not self.isGameOver:
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

        if self.isGameOver:
            self.drawGameOverText(screen, cellSize)

    def checkCollision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomFruit()
            self.snake.addBlock()
            self.snake.score += 1
            self.snake.playCrunchSound()

        if self.fruit.pos == self.snakeAI.body[0]:
            self.fruit.randomFruit()
            self.snakeAI.addBlock()
            self.snakeAI.score += 1
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
                self.gameOver(1)

        for block in self.snakeAI.body[1:]:
            if block == self.snakeAI.body[0]:
                self.gameOver(2)

        # Check if the snake hits the other snake
        for block in self.snakeAI.body[0:]:
            if self.snake.body[0] == block:
                self.gameOver(3)

        for block in self.snake.body[0:]:
            if self.snakeAI.body[0] == block:
                self.gameOver(4)

    def gameOver(self, case):
        if(case == 1):
            # Player hits itself
            self.snake.score /= 2
        elif(case == 2):
            # AI snake hits itself
            self.snakeAI.score /= 2
        elif(case == 3):
            # Player hits AI snake
            self.snakeAI.score += 5
        elif(case == 4):
            # AI snake hits player
            self.snake.score += 5

        self.isGameOver = True        
        #self.snake.reset()
        #self.snakeAI.reset()

    def drawGameOverText(self, screen, cellSize):
        gameOverText = self.gameFontLarge.render("Game Over", True, (56,74,12))
        gameOverRect = gameOverText.get_rect(center = (self.cellNumber*cellSize / 2, self.cellNumber*cellSize / 2))
        
        if self.snake.score > self.snakeAI.score:
            winnerText = self.gameFontMedium.render("Player wins!", True, (56,74,12))
        elif self.snakeAI.score > self.snake.score:
            winnerText = self.gameFontMedium.render("AI wins!", True, (56,74,12))
        else:
            winnerText = self.gameFontMedium.render("Draw", True, (56,74,12))
        winnerRect = winnerText.get_rect(center = (self.cellNumber*cellSize / 2, (self.cellNumber*cellSize / 2) + 100))

        resetText = self.gameFontSmall.render("Press 'R' to start a new game", True, (56,74,12))
        resetRect = gameOverText.get_rect(center = ((self.cellNumber*cellSize / 2) + 150, (self.cellNumber*cellSize / 2) + 400))

        screen.blit(gameOverText, gameOverRect)
        screen.blit(winnerText, winnerRect)
        screen.blit(resetText, resetRect)

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
        scoreText = str(self.snakeAI.score)
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
        scoreText = str(self.snake.score)
        scoreSurface = self.gameFont.render(scoreText, True, (56,74,12))
        scorePosition = Vector2(94, int(cellSize * self.cellNumber - 40))
        scoreRect = scoreSurface.get_rect(center = (scorePosition.x, scorePosition.y))
        appleRect = self.apple.get_rect(midright = (scoreRect.left, scoreRect.centery))
        bgRect = pygame.Rect(appleRect.left, appleRect.top, appleRect.width + scoreRect.width + 6, appleRect.height)

        pygame.draw.rect(screen, (167,209,61), bgRect)
        pygame.draw.rect(screen, (83,148,250), bgRect, 2)
        screen.blit(scoreSurface, scoreRect)
        screen.blit(self.apple, appleRect)