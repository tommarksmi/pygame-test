import pygame
from pygame.locals import *
import entities
import sys
import random
import constants

# TODO: create game initializer class to make it easier to setup each level
# and redraw gameboard from with in game.

pygame.init()
const = constants.Constants()

FramePerSec = pygame.time.Clock()
display_surface = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
pygame.display.set_caption("Game")


def populate_coins(numb_of_coins: int, coin_color: tuple) -> list:
    coins = []
    for num in range(0, numb_of_coins):
        coin = entities.Coin(coin_color)
        coins.append(coin)
    return coins


goal = entities.Goal(const.WIDTH, const.HEIGHT, const.YELLOW, 'top')
goal_2 = entities.Goal(const.WIDTH, const.HEIGHT, const.LIGHT_BLUE, 'bottom')
goal_group = pygame.sprite.Group(goal, goal_2)

bounding_box_goal = entities.Bounding_box(goal)
bounding_box_goal_2 = entities.Bounding_box(goal_2)
bounding_boxes = pygame.sprite.Group(bounding_box_goal, bounding_box_goal_2)

player = entities.Player(const.FRICTION, const.ACCEL, const.WIDTH, const.HEIGHT)
yellow_coins = populate_coins(10, const.YELLOW)
blue_coins = populate_coins(10, const.LIGHT_BLUE)
coins = []
coins.extend(blue_coins)
coins.extend(yellow_coins)
coin_group = pygame.sprite.Group(coins)
collected_coins = pygame.sprite.Group()

print('goal pos values: ' + str(goal.pos.x) + str(goal.pos.y))
print(goal.pos)

player.pos.x = const.WIDTH / 2
player.pos.y = const.HEIGHT / 2

for coin in coins:
    # Adding a buffer around the border of the main game baord to ensure coins don't display half off screen
    coin.pos.x = random.randint(0 + (coin.rect.width * 2) , const.WIDTH - (coin.rect.width * 2))
    coin.pos.y = random.randint(0 + (coin.rect.height * 2) + 40, const.HEIGHT - (coin.rect.height * 2) - 40)
    display_surface.blit(coin.surf, coin.pos)
    coin.move()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display_surface.fill((0, 0, 0))
    display_surface.blit(goal.surf, goal.pos)
    display_surface.blit(goal_2.surf, goal_2.pos)
    display_surface.blit(player.surf, player.pos)

    for coin in coins:
        display_surface.blit(coin.surf, coin.pos)
    pygame.display.update()
    collided_coins = pygame.sprite.spritecollide(player, coin_group, True)

    if len(collided_coins) > 0 and player.coin_count == 0:
        collected_coins.add(collided_coins[0])
        player.coin_count += 1
        # print('collected_coins updated!' + str(type(collected_coins)))
        print('Coin count: ' + str(len(collected_coins)))

    for coin in collected_coins:
        coin.pos = player.pos.x + 10, player.pos.y + 10

    collided_goal = pygame.sprite.spritecollide(player, goal_group, True)

    if len(collided_goal) > 0 and len(collected_coins) > 0:
        if collided_goal[0].color_code == collided_coins[0].color_code:
            print('correct color coin returned to goal')



    FramePerSec.tick(const.FPS)
    player.move()
