import pygame
from pygame.locals import *
import time
import entities
import sys

pygame.init()
vector = pygame.math.Vector2

HEIGHT = 450
WIDTH = 400
ACCEL = 0.5
FRICTION = -0.12
FPS = 60

FramePerSec = pygame.time.Clock()

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

player = entities.player(FRICTION, ACCEL, WIDTH, HEIGHT)
coin = entities.coin()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display_surface.fill((0, 0, 0))

    display_surface.blit(player.surf, player.rect)
    display_surface.blit(coin.surf, (50, 50))

    pygame.display.update()
    FramePerSec.tick(FPS)
    player.move()
