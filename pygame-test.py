import pygame
from pygame.locals import *
import entities
import sys
import random

pygame.init()
vector = pygame.math.Vector2

HEIGHT = 900
WIDTH = 800
ACCEL = 0.25
FRICTION = -0.12
FPS = 120

FramePerSec = pygame.time.Clock()
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


def populate_coins():
    coin1 = entities.Coin()
    coin2 = entities.Coin()
    coin3 = entities.Coin()
    return [coin1, coin2, coin3]


player = entities.Player(FRICTION, ACCEL, WIDTH, HEIGHT)
coins = populate_coins()
coin_group = pygame.sprite.Group(coins)
collected_coins = pygame.sprite.Group()

goal = entities.Goal(WIDTH)
# goal.place_goal((WIDTH / 3, 0))
print('goal pos values: ' + str(goal.pos.x) + str(goal.pos.y))
print(goal.pos)

player.pos.x = WIDTH / 2
player.pos.y = HEIGHT / 2

for coin in coins:
    coin.pos.x = random.randint(0, WIDTH)
    coin.pos.y = random.randint(0, HEIGHT)
    display_surface.blit(coin.surf, coin.pos)
    coin.move()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            print('coins list: ' + str(coins))
            print('sprite group of coins: ' + str(coin_group))
            print('collected_coins: ' + str(collected_coins))
            pygame.quit()
            sys.exit()

    display_surface.fill((0, 0, 0))
    display_surface.blit(goal.surf, goal.pos)
    display_surface.blit(player.surf, player.pos)

    for coin in coins:
        display_surface.blit(coin.surf, coin.pos)
    pygame.display.update()
    collided_coins = pygame.sprite.spritecollide(player, coin_group, True)

    if len(collided_coins) > 0:
        collected_coins.add(collided_coins)
        print('collected_coins updated!' + str(type(collected_coins)))

    for coin in collected_coins:
        coin.pos = player.pos.x + 10, player.pos.y + 10

    FramePerSec.tick(FPS)
    player.move()
