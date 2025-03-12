import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

playerX = 400
playerY = 300
step = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)

clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)
    screen.blit(screen, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        playerY -= step

    if pressed[pygame.K_DOWN]:
       playerY += step

    if pressed[pygame.K_LEFT]:
        playerX -= step

    if pressed[pygame.K_RIGHT]:
        playerX += step

    if playerX >= 775:
        playerX = 775
    elif playerX <= 25:
        playerX = 25

    if playerY >= 575:
        playerY = 575
    elif playerY <= 25:
        playerY = 25



    player = pygame.draw.circle(screen, RED, (playerX, playerY), 25)

    clock.tick(30)

    pygame.display.flip()
