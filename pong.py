import pygame
from pygame.locals import *
import sys
import random

# SIZE OF THE SCREEN
WIDTH = 600
HEIGHT = 500

# FPS
FPS = 60

UP, DOWN, UPRIGHT, DOWNRIGHT, DOWNLEFT, UPLEFT = 0,1,2,3,4,5
START, STOP = 0, 1

# Speed of Paddle
PADDLEMOVEMENT = 10
# Speed of Ball
BALLMOVEMENT = 3

# SCREEN
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

# Position X of the Paddle
PADDLESTARTPOS = 30
PADDLEWIDTH = 10
PADDLEHEIGHT = 60

BALLSIZE = 7

class Ball():
    def __init__(self):
        # Sets random  start orientation
        self.orientation = random.randint(2,5)

        self.draw(WIDTH/2, HEIGHT/2)
        
    def update(self):
        xPosition = self.rect.center[0]
        yPosition = self.rect.center[1]

        halfHeight = self.rect.width/2
        halfWidth = self.rect.width/2

        # Ball hit top border
        if((yPosition - halfHeight - BALLMOVEMENT) < 0):
            self.doWhenHitBorder(self.orientation)

        # Ball hit bottom border
        if((yPosition + halfHeight + BALLMOVEMENT) > HEIGHT):
            self.doWhenHitBorder(self.orientation)            

        if(self.orientation == UPRIGHT):
            self.dy = -BALLMOVEMENT
            self.dx = BALLMOVEMENT
        if(self.orientation == DOWNRIGHT):
            self.dy = BALLMOVEMENT
            self.dx = BALLMOVEMENT
        if(self.orientation == UPLEFT):
            self.dy = -BALLMOVEMENT
            self.dx = -BALLMOVEMENT
        if(self.orientation == DOWNLEFT):
            self.dy = BALLMOVEMENT
            self.dx = -BALLMOVEMENT

        self.draw(xPosition + self.dx, yPosition + self.dy)

    def doWhenHitBorder(self, direction):
        if(direction == UPRIGHT):
            self.orientation = DOWNRIGHT
        elif(direction == UPLEFT):
            self.orientation = DOWNLEFT
        elif(direction == DOWNRIGHT):
            self.orientation = UPRIGHT
        elif(direction == DOWNLEFT):
            self.orientation = UPLEFT

    def doWhenHitPaddle(self):
        if(self.orientation == DOWNRIGHT): self.orientation = DOWNLEFT
        elif(self.orientation == UPRIGHT): self.orientation = UPLEFT
        elif(self.orientation == UPLEFT): self.orientation = UPRIGHT
        elif(self.orientation == DOWNLEFT): self.orientation = DOWNRIGHT

    def draw(self, x, y):
        self.rect = pygame.draw.circle(SCREEN, (255,255,255), (x, y), BALLSIZE)

class Paddle():
    def __init__(self, left):
        self.left = left
        self.top = HEIGHT/2 - PADDLEHEIGHT/2
        
        self.dy = 0
        self.draw(self.left, self.top)
        
    def update(self):
        # New top is actual Y Position + new Y Position
        newTop = self.top + self.dy

        # Limit movement out of bounds
        if((newTop + PADDLEHEIGHT) > HEIGHT):
            newTop = HEIGHT - PADDLEHEIGHT
        if(newTop<0):
            newTop = 0

        self.top = newTop
        self.draw(self.left, newTop)
        
    def draw(self, left, top):
        self.rect = pygame.draw.rect(SCREEN, (255,255,255), (left, top, PADDLEWIDTH, PADDLEHEIGHT))

    def steer(self, direction, operation):
        if operation == STOP:
            self.dy = 0
        elif operation == START:
            self.dy = {UP: -PADDLEMOVEMENT, DOWN: PADDLEMOVEMENT}[direction]

class Game():
    
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Fill background
        self.background = pygame.Surface(SCREEN.get_size()).convert()

        # Initialize clock
        self.clock = pygame.time.Clock()

        # Font configuration
        self.font = pygame.font.SysFont("monospace", 40)
    
    def quit(self):
        pygame.quit()
        sys.exit(0)

def main():
    # Creates the game
    game = Game()

    # Define all Sprites
    ball = Ball()
    barLeft = Paddle(PADDLESTARTPOS)
    barRight = Paddle(WIDTH - PADDLESTARTPOS - 20)

    # Define all Texts
    textPlayer1Wins = game.font.render("Player 1 Wins", True, (255,255,255))
    textPlayer2Wins = game.font.render("Player 2 Wins", True, (255,255,255))

    while True:
        # Define FPS
        game.clock.tick(FPS)

        # Handle Keyboard events
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                game.quit()
            if event.type == KEYDOWN:
                if event.key == K_DOWN: barRight.steer(DOWN, START)
                if event.key == K_UP: barRight.steer(UP, START)
                if event.key == K_s: barLeft.steer(DOWN, START)
                if event.key == K_w: barLeft.steer(UP, START)

            if event.type == KEYUP:
                if event.key == K_DOWN: barRight.steer(DOWN, STOP)
                if event.key == K_UP: barRight.steer(UP, STOP)
                if event.key == K_s: barLeft.steer(DOWN, STOP)
                if event.key == K_w: barLeft.steer(UP, STOP)

        # If ball hit the Left Paddle or Right Paddle
        if((ball.rect.colliderect(barLeft.rect)) or (ball.rect.colliderect(barRight.rect))):
            ball.doWhenHitPaddle()

        # Draw background
        SCREEN.blit(game.background, (0, 0))

        # If Ball hits left border
        if(ball.rect[0] <= BALLMOVEMENT):
            SCREEN.blit(textPlayer2Wins,(WIDTH / 2 - (textPlayer2Wins.get_width() / 2), HEIGHT / 2 - (textPlayer2Wins.get_height() / 2)))
            pygame.display.update()
            pygame.time.wait(3000)
            ball = Ball()

        # If Ball hits right border
        if(ball.rect[0] >= (WIDTH - BALLMOVEMENT - ball.rect.width)):
            SCREEN.blit(textPlayer1Wins,(WIDTH / 2 - (textPlayer1Wins.get_width() / 2), HEIGHT / 2 - (textPlayer1Wins.get_height() / 2)))
            pygame.display.update()
            pygame.time.wait(3000)
            ball = Ball()

        barLeft.update()
        barRight.update()
        ball.update()

        pygame.display.update()

    game.quit()

if __name__ == '__main__':
    main()