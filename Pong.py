import pygame
import sys
import random 
import math

pygame.init()
pygame.font.init()

font = pygame.font.Font(None, 30)

windowHeight = 600
windowLength = 1000
screen = pygame.display.set_mode((windowLength,windowHeight))

radius = 10
speed = 0
playerOffset = 50
player1 = {"x": playerOffset, "y": 50, "Acc": 50, "Score": 0, "height": 100, "width": 10}
player2 = {"x": windowLength - playerOffset, "y": 50, "Acc": 50, "Score": 0, "height": 100, "width": 10}
Ball = {"x": 400, "y": 200, "mx": 1, "my": 0.4, "multiplier": 100, "p1Expected": False, "hits": 0, 
        "maxAngle": 40, "minAngle": -40}
player1Box = (player1["x"], player1["y"], player1["width"], player1["height"])
player2Box = (player2["x"], player2["y"], player2["width"], player2["height"])
ballRect = pygame.Rect(Ball["x"]-radius, Ball["y"]-radius, 30, 30)





def Controls1():
    global speed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    if keys[pygame.K_w]:
        player1["y"] = player1["y"] - player1["Acc"] * speed
    if keys[pygame.K_s]:
        player1["y"] = player1["y"] + player1["Acc"] * speed


def Controls2():
    global speed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    if keys[pygame.K_UP]:
        player2["y"] = player2["y"] - player2["Acc"] * speed
    if keys[pygame.K_DOWN]:
        player2["y"] = player2["y"] + player2["Acc"] * speed

def ScreenUpdate():
    screen.fill((0,0,0))
    global player1Box
    global player2Box
    player1Box = (player1["x"], player1["y"], player1["width"], player1["height"])
    player2Box = (player2["x"], player2["y"], player2["width"], player2["height"])
    pygame.draw.rect(screen, (255, 0, 0), player1Box)
    pygame.draw.rect(screen, (0, 255, 0), player2Box)
    pygame.draw.circle(screen, (255,255,255), (Ball["x"], Ball["y"]), radius)
    global ballRect
    ballRect = pygame.Rect(Ball["x"]-radius, Ball["y"]-radius, radius*2, radius*2)
    

def BallMovement():
    global speed
    global ballRect
    global player1Box
    global player2Box
    if ballRect.colliderect(player2Box) and Ball["p1Expected"] == False:
        Ball["p1Expected"] = True
        calcBallDirection(player2)
        Ball["hits"] += 1
    if ballRect.colliderect(player1Box) and Ball["p1Expected"]:
        Ball["p1Expected"] = False
        calcBallDirection(player1)
        Ball["hits"] += 1
    if ballRect.top <= 0 or ballRect.bottom >= windowHeight:
        Ball["my"] *= -1
    Ball["x"] = Ball["x"] + Ball["mx"] * Ball["multiplier"] * speed
    Ball["y"] = Ball["y"] + Ball["my"] * Ball["multiplier"] * speed
        

def gameStateCheck():
    global ballRect
    global player1
    global player2
    playerBound(player1)
    playerBound(player2)
    ballOut()

def playerBound(player):
    if player["y"] < 0:
        player["y"] = 0
    if player["y"] + player["height"] > windowHeight:
        player["y"] = windowHeight - player["height"]

def ballOut():
    if Ball["x"] < radius:
        player2["Score"] += 1
        Ball["p1Expected"] = False
        ballSet()
        playerSet()
        Ball["hits"] = 0
    if Ball["x"] > windowLength-radius:
        player1["Score"] += 1
        Ball["p1Expected"] = True
        ballSet()
        playerSet()
        Ball["hits"] = 0


def playerSet():
    player1["y"] = windowHeight / 2 - player1["height"]/2
    player2["y"] = windowHeight / 2 - player2["height"]/2

def ballSet():
    angle = random.randrange(Ball["minAngle"], Ball["maxAngle"]) * math.pi / 180
    Ball["mx"] = math.cos(angle)
    Ball["my"] = math.sin(angle) * -1
    print((angle, Ball["mx"], Ball["my"], Ball["p1Expected"]))
    if Ball["p1Expected"]:
        Ball["mx"] *= -1
    elif Ball["mx"] < 0:
        Ball["mx"] *= -1
    Ball["x"], Ball["y"] = windowLength / 2, windowHeight/2
    
def scorePrint():
    p1Score = font.render(str(player1["Score"]), True, (255,255,255))
    screen.blit(p1Score, (10, 10))
    p2Score = font.render(str(player2["Score"]), False, (255,255,255))
    screen.blit(p2Score, (windowLength-20, 10))
    hits = font.render(str(Ball["hits"]), True, (255, 255,255))
    screen.blit(hits, (windowLength /2,10))
    

def calcBallDirection(player):
    playerCenter = player["y"] + player["height"]/2
    maxDist, minDist = player["height"] / 2, player["height"] / 2 * -1 
    ballDist = playerCenter - Ball["y"]
    angle = (((ballDist-(minDist))*(Ball["maxAngle"]-Ball["minAngle"]))/(maxDist-minDist) + Ball["minAngle"]) * math.pi / 180
    Ball["mx"] = math.cos(angle) * -1
    Ball["my"] = math.sin(angle) * -1
    if Ball["p1Expected"] == False:
        Ball["mx"] *= -1
    print(angle)

clock = pygame.time.Clock()
playerSet()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    dt = clock.tick(60)
    # convert the delta to seconds (for easier calculation)
    speed = 1 / float(dt)
    BallMovement()
    Controls1()
    Controls2()
    playerBound(player1)
    playerBound(player2)
    ScreenUpdate()
    gameStateCheck()
    scorePrint()
    pygame.display.flip()
    pygame.display.update()
