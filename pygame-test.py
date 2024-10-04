import pygame
from pygame.locals import *
import entities
import sys
import random
import constants
import pygame_widgets
from pygame_widgets.button import Button

# TODO: create game initializer class to make it easier to setup each level
# and redraw gameboard from with in game.

pygame.init()
const = constants.Constants()

bkg_img = pygame.image.load('game-background.jpg')
img_rect = bkg_img.get_rect()

FramePerSec = pygame.time.Clock()
display_surface = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
pygame.display.set_caption("Game")


def generate_coins(numb_of_coins: int, coin_color: tuple) -> list:
    populated_coins = []
    for num in range(0, numb_of_coins):
        new_coin = entities.Coin(coin_color)
        populated_coins.append(new_coin)
    return populated_coins

def populate_coins() -> list:
    coins = []
    yellow_coins = generate_coins(1, const.YELLOW)
    blue_coins = generate_coins(0, const.LIGHT_BLUE)
    coins.extend(blue_coins)
    coins.extend(yellow_coins)
    return coins

def reset_game(g_round: entities.GameRound):
    player.pos.x = const.WIDTH / 2
    player.pos.y = const.HEIGHT / 2
    g_round.update_coins_in_play(populate_coins())
    coin_layout(g_round.coins_in_play)

def coin_layout(coins: list):
        # move loop into function and take a list of coins in then call from reset method
    for coin in coins:
        # Adding a buffer around the border of the main game board to ensure coins don't display half off-screen
        coin.pos.x = random.randint(0 + (coin.rect.width * 2) , const.WIDTH - (coin.rect.width * 2))
        coin.pos.y = random.randint(0 + (player.rect.height * 2) + 40, const.HEIGHT - (player.rect.height * 2) - 40)
        # display_surface.blit(coin.surf, coin.pos)
        coin.move()

def quit_game():
    pygame.quit()
    sys.exit()

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

coins = populate_coins()
# coin_imgs = load_coin_imgaes()

game_round = entities.GameRound(coins)

# coin_group = pygame.sprite.Group(game_round.coins_in_play)
collected_coins = pygame.sprite.Group()

print('goal pos values: ' + str(goal.pos.x) + str(goal.pos.y))
print(goal.pos)

player.pos.x = const.WIDTH / 2
player.pos.y = const.HEIGHT / 2


coin_layout(game_round.coins_in_play)

restart_button = Button(
    display_surface,
    const.WIDTH / 2,
    const.HEIGHT / 2,
    125,
    30,
    text= 'Play Again',
    onClick=lambda: reset_game(game_round)
    )

exit_button = Button(
    display_surface,
    const.WIDTH / 2 - 150,
    const.HEIGHT / 2,
    125,
    30,
    text= 'Exit',
    onClick=lambda: quit_game()
    )

animation_tick_count = 0
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display_surface.blit(bkg_img, img_rect)
    display_surface.blit(goal.surf, goal.pos)
    goal.place_goal(goal.pos)
    display_surface.blit(goal_2.surf, goal_2.pos)
    goal_2.place_goal(goal_2.pos)

    if len(collected_coins) > 0:
        for c in collected_coins:
            display_surface.blit(c.image, c.rect.topleft)

    display_surface.blit(player.surf, player.pos)

    for coin in game_round.coins_in_play:
        display_surface.blit(coin.image, coin.rect.topleft)
    collided_coins = pygame.sprite.spritecollide(player, game_round.coin_group, False)
    collided_goal = pygame.sprite.spritecollide(player, goal_group, False)

    # Animations triggered here
    if animation_tick_count % 10 == 0:
        for coin in game_round.coins_in_play:
            coin.update_image()
    animation_tick_count += 1
    #

    # Check for player coin collision if true update player coin count
    if len(collided_coins) > 0 and player.coin_count == 0:
        held_coin = collided_coins.pop()
        collected_coins.add(held_coin)
        player.coin_count += 1

    # Checks for collision with goal while holding a coin
    if len(collided_goal) > 0 and held_coin:
        if collided_goal[0].color_code == held_coin.color_code:
            collected_coins.remove(held_coin)
            game_round.coin_group.remove(held_coin)
            game_round.coins_in_play.remove(held_coin)
            player.coin_count -= 1
            held_coin = None

    for coin in collected_coins:
        # coin.rect.center = player.pos.x + 10, player.pos.y + 10
        coin.rect.center = player.rect.center

    if len(game_round.coins_in_play) <= 0:
        pygame_widgets.update(events)
        player.stop()
    else:
        player.move()
        coin_layout

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_i]:
        print('Mouse position: ' + str(pygame.mouse.get_pos()))
        print('Collected coins len: ' + str(len(collected_coins)))
        print('Collided coins len: ' + str(len(collided_coins)))
        # # print('Collided goals len: ' + str(len(collided_goal)))
        print('len of coins: ' + str(len(game_round.coins_in_play)))
        print('held coin: ' + str( held_coin if held_coin else 'none'))
        print('player coin count: ' + str(player.coin_count))
        # print('coins: ' + str(coins))
        # print('player pos: ' + str(player.pos))
        for c in collided_coins:
            print(str(c))
        print('len of collided_coins: ' + str(len(collected_coins)))
        # for coin in coins:
        #     print('coin at: ' + str(coin.pos))

    FramePerSec.tick(const.FPS)
    pygame.display.update()
