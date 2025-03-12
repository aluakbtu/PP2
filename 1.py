import pygame
from datetime import datetime

pygame.init()
S_WIDTH = 600
S_HIGHT = 600
PLACE = (S_WIDTH / 2, S_HIGHT / 2)

screen = pygame.display.set_mode((S_WIDTH, S_HIGHT))
done = True

FPS = 60
clocks = pygame.time.Clock()

WHITE = (255, 255, 255)

clock = pygame.image.load("/Users/askarovva/Desktop/Lab7 programming/clock.jpg")
CL_WIDTH = 500
CL_HIGHT = 500
CL_POS_X = S_WIDTH / 2 - CL_WIDTH / 2
CL_POS_Y = S_HIGHT / 2 - CL_HIGHT / 2

big_arrow = pygame.image.load("/Users/askarovva/Desktop/Lab7 programming/big_arrow.png")
BA_WIDTH = 35
BA_RATIO = 0.14
BA_HIGHT = BA_WIDTH / BA_RATIO
big_arrow = pygame.transform.scale(big_arrow, (BA_WIDTH, BA_HIGHT))

ba_rect = big_arrow.get_rect()
ba_rect.center = PLACE

small_arrow = pygame.image.load("/Users/askarovva/Desktop/Lab7 programming/small_arrow.png")
SA_WIDTH = 50
SA_RATIO = 0.3
SA_HIGHT = SA_WIDTH / SA_RATIO
small_arrow = pygame.transform.scale(small_arrow, (SA_WIDTH, SA_HIGHT))

sa_rect = small_arrow.get_rect()
sa_rect.center = PLACE

while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False

    angle = datetime.now().second * -6
    screen.fill(WHITE)
    screen.blit(clock, (CL_POS_X, CL_POS_Y))
    rotated_ba = pygame.transform.rotate(big_arrow, angle)
    rotated_ba_rect = rotated_ba.get_rect()
    rotated_ba_rect.center = ba_rect.center
    screen.blit(rotated_ba, rotated_ba_rect)   

    angle_2 = datetime.now().minute * -6
    rotated_sa = pygame.transform.rotate(small_arrow, angle_2)
    rotated_sa_rect = rotated_sa.get_rect()
    rotated_sa_rect.center = sa_rect.center
    screen.blit(rotated_sa, rotated_sa_rect)    
    

    pygame.display.flip()
    clocks.tick(FPS)
