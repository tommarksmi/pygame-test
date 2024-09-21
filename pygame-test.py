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
    populated_coins = []
    for num in range(0, numb_of_coins):
        new_coin = entities.Coin(coin_color)
        populated_coins.append(new_coin)
    return populated_coins

goals = []
goal = entities.Goal(const.WIDTH, const.HEIGHT, const.YELLOW, 'top')
goal_2 = entities.Goal(const.WIDTH, const.HEIGHT, const.LIGHT_BLUE, 'bottom')
goals.append(goal)
goals.append(goal_2)
goal_group = pygame.sprite.Group(goals)

bounding_box_goal = entities.BoundingBox(goal)
bounding_box_goal_2 = entities.BoundingBox(goal_2)
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
    # Adding a buffer around the border of the main game board to ensure coins don't display half off-screen
    coin.pos.x = random.randint(0 + (coin.rect.width * 2) , const.WIDTH - (coin.rect.width * 2))
    coin.pos.y = random.randint(0 + (player.rect.height * 2) + 40, const.HEIGHT - (player.rect.height * 2) - 40)
    display_surface.blit(coin.surf, coin.pos)
    coin.move()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display_surface.fill((0, 0, 0))

    display_surface.blit(goal.surf, goal.pos)
    goal.place_goal(goal.pos)
    display_surface.blit(goal_2.surf, goal_2.pos)
    goal_2.place_goal(goal_2.pos)

    display_surface.blit(player.surf, player.pos)
    for coin in coins:
        display_surface.blit(coin.surf, coin.pos)
    pygame.display.update()
    collided_coins = pygame.sprite.spritecollide(player, coin_group, False)
    collided_goal = pygame.sprite.spritecollide(player, goal_group, False)


    # Check for player coin collision if true udpate player coin count
    if len(collided_coins) > 0 and player.coin_count == 0:
        held_coin = collided_coins.pop()
        print('held coin updated...')
        #TODO find a way to clear contents of collected_coins before adding the new held coin
        collected_coins.add(held_coin)
        player.coin_count += 1

    # Checks for collision with goal while holding a coin
    if len(collided_goal) > 0 and held_coin:
        print('player goal collision')
        # held_coin = collected_coins.sprites()[0]
        # print('held coind updated: ' + str(held_coin))
        print('goal color: ' + str(collided_goal[0].color_code) + '  coin color: ' + str(held_coin.color_code))
        if collided_goal[0].color_code == held_coin.color_code:
            collected_coins.remove(held_coin)
            collected_coins.empty()
            coins.remove(held_coin)
            print('held coin removed')
            player.coin_count -= 1
            held_coin = None

    for coin in collected_coins:
            coin.pos = player.pos.x + 10, player.pos.y + 10

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_i]:
        # print('Collected coins len: ' + str(len(collected_coins)))
        # print('Collided coins len: ' + str(len(collided_coins)))
        # print('Collided goals len: ' + str(len(collided_goal)))
        print('len of coins: ' + str(len(coins)))
        # print('coins: ' + str(coins))
        print('player pos: ' + str(player.pos))
        for c in collided_coins:
            print(str(c))
        print('len of collided_coins: ' + str(len(collected_coins)))

        try:
            if (held_coin):
                print('held coin color: ' + str(held_coin.color_code))
        except:
            print('held_coin not assigned nothing to print')
        # for coin in coins:
        #     print('coin at: ' + str(coin.pos))



    FramePerSec.tick(const.FPS)
    player.move()
