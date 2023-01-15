import pygame
import sys
import random 
import math

class Player:
    def __init__(self, x=50, y=50, Acc=50, Score=0, height=100, width=10):
        self.x = x
        self.y = y
        self.Acc = Acc
        self.Score = Score
        self.height = height
        self.width = width
        self.box = (self.x, self.y, self.width, self.height)
    
    def Controls1(self, speed):
        speed = speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_w]:
            self.y = self.y - self.Acc * speed
        if keys[pygame.K_s]:
            self.y = self.y + self.Acc * speed

    def Controls2(self, speed):
        speed = speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_UP]:
            self.y = self.y - self.Acc * speed
        if keys[pygame.K_DOWN]:
            self.y = self.y + self.Acc * speed
        

class Ball:
    def __init__(self, x=400, y=200, mx=1, my=0.4, multiplier=100, p1Expected=False, hits=0, maxAngle=40, minAngle=-40, radius=10) -> None:
        self.x = x
        self.y = y
        self.mx = mx
        self.my = my
        self.multiplier = multiplier
        self.p1Expected = p1Expected
        self.hits = hits
        self.maxAngle = maxAngle
        self.minAngle = minAngle
        self.radius = radius
        self.rect = pygame.Rect(self.x-self.radius, self.y-self.radius, 30, 30)
    
    def movement(self, player1, player2, game):
        self.player1 = player1
        self.player2 = player2
        game = game
        if self.rect.colliderect(self.player2.box) and self.p1Expected == False:
            self.p1Expected = True
            self.calcBallDirection(self.player2)
            self.hits += 1
        if self.rect.colliderect(self.player1.box) and self.p1Expected:
            self.p1Expected = False
            self.calcBallDirection(self.player1)
            self.hits += 1
        if self.rect.top <= 0 or self.rect.bottom >= game.windowHeight:
            self.my *= -1
        self.x = self.x + self.mx * self.multiplier * game.speed
        self.y = self.y + self.my * self.multiplier * game.speed

    def calcBallDirection(self, player):
        player = player
        playerCenter = player.y + player.height/2
        maxDist, minDist = player.height / 2, player.height / 2 * -1
        ballDist = playerCenter - self.y
        angle = (((ballDist-(minDist))*(self.maxAngle-self.minAngle))/(maxDist-minDist) + self.minAngle) * math.pi / 180
        self.mx = math.cos(angle) * -1
        self.my = math.sin(angle) * -1
        if self.p1Expected == False:
            self.mx *= -1
        

class Game:
    def __init__(self, windowHeight=600, windowLength=1000, speed=0, playerOffset=50,) -> None:
        self.windowHeight = windowHeight
        self.windowLength = windowLength
        self.screen = pygame.display.set_mode((self.windowLength, self.windowHeight))
        self.speed = speed
        self.playerOffset = playerOffset
        self.player1 = Player()
        self.player2 = Player(x=self.windowLength-self.playerOffset)
        self.ball = Ball()
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(None, 30)
        self.clock = pygame.time.Clock()
        self.playerSet()
        self.ballSet()
    
    def Update(self):       
        self.screen.fill((0,0,0))
        self.player1.box = (self.player1.x, self.player1.y, self.player1.width, self.player1.height)
        self.player2.box = (self.player2.x, self.player2.y, self.player2.width, self.player2.height)
        pygame.draw.rect(self.screen, (255, 0, 0), self.player1.box)
        pygame.draw.rect(self.screen, (0, 255, 0), self.player2.box)
        pygame.draw.circle(self.screen, (255,255,255), (self.ball.x, self.ball.y), self.ball.radius)
        self.ball.rect = pygame.Rect(self.ball.x-self.ball.radius, self.ball.y-self.ball.radius, 
        self.ball.radius*2, self.ball.radius*2)
        self.scorePrint()
        pygame.display.update()
        pygame.display.flip()
    
    def playerBound(self, player):
        player = player
        if player.y < 0:
            player.y = 0
        if player.y + player.height > self.windowHeight:
            player.y = self.windowHeight - player.height

    def ballOut(self):
        if self.ball.x < self.ball.radius:
            self.player2.Score += 1
            self.ball.p1Expected = False
            self.ballSet()
            self.playerSet()
            self.ball.hits = 0
        if self.ball.x > self.windowLength-self.ball.radius:
            self.player2.Score += 1
            self.ball.p1Expected = True
            self.ballSet()
            self.playerSet()
            self.ball.hits = 0

    def stateCheck(self):
        self.playerBound(self.player1)
        self.playerBound(self.player2)
        self.ballOut()
    
    def playerSet(self):
        self.player1.y = self.windowHeight / 2 - self.player1.height/2
        self.player2.y = self.windowHeight / 2 - self.player2.height/2

    def ballSet(self):
        angle = random.randrange(self.ball.minAngle, self.ball.maxAngle) * math.pi / 180
        self.ball.mx = math.cos(angle)
        self.ball.my = math.sin(angle) * -1
        if self.ball.p1Expected:
            self.ball.mx *= -1
        elif self.ball.mx < 0:
            self.ball.mx *= -1
        self.ball.x, self.ball.y = self.windowLength / 2, self.windowHeight/2

    def scorePrint(self):
        p1Score = self.font.render(str(self.player1.Score), True, (255,255,255))
        self.screen.blit(p1Score, (10, 10))
        p2Score = self.font.render(str(self.player2.Score), False, (255,255,255))
        self.screen.blit(p2Score, (self.windowLength-20, 10))
        hits = self.font.render(str(self.ball.hits), True, (255, 255,255))
        self.screen.blit(hits, (self.windowLength /2,10))
    
    def runStep(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
        dt = self.clock.tick(60)
        self.speed = 1 / float(dt)
        self.ball.movement(player1=self.player1, player2=self.player2, game=self)
        self.player1.Controls1(self.speed)
        self.player2.Controls2(self.speed)
        self.playerBound(self.player1)
        self.playerBound(self.player2)
        self.stateCheck()
        self.Update()


game = Game()

while True:
    game.runStep()
