import pygame
import random
import math

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('2833951.jpg')

# title and icon
pygame.display.set_caption("space wars")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load("space-invaders.png")
playerx = 370
playery = 480
playerx_change = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyimg.append(pygame.image.load("ufo.png"))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(-0.4)
    enemyy_change.append(40)

# bullet
bulletimg = pygame.image.load("bullet.png")
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 10
bullet_state = "ready"  # ready-you cant see bullet on the screen # fire-bullet is moving

# score = 0

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow(enemyx - bulletx, 2) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    screen.fill((227, 113, 245))
    # background img
    screen.blit(background, (0, 0))
    # playerx-=0.09
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.5

            if event.key == pygame.K_RIGHT:
                playerx_change = +0.5

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletx = playerx
                    fire_bullet(bulletx, playery)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # checking for boundries
    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    # enemy movement

    for i in range(number_of_enemies):

        # game over
        if enemyy[i] > 440:
            for j in range(number_of_enemies):
                enemyy[j] = 3000
            game_over_text()
            break

        enemyx[i] += enemyx_change[i]

        if enemyx[i] <= 0:
            enemyx_change[i] = 0.4
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -0.4
            enemyy[i] += enemyy_change[i]

        # collision
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx[i], enemyy[i], i)

    # bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()
