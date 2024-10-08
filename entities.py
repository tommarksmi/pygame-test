import sys
import pygame
import pathlib
import os
from pygame.locals import *


class Goal(pygame.sprite.Sprite):

    vector = pygame.math.Vector2

    def __init__(self, parent_width, parent_height, color: tuple, vert_position: str):
        super().__init__()
        self.color_code = color
        self.height = 40
        self.width = parent_width / 3
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(self.color_code)
        self.pos = self.vector(parent_width/3, self.calc_vert_pos(parent_height, vert_position))
        self.rect = self.surf.get_rect()

        green = (0, 255, 0)
        blue = (0, 0, 128)

        self.font = pygame.font.Font('freesansbold.ttf', 28)
        self.text = self.font.render('GOAL', True, green, blue)
        self.text_rect = self.text.get_rect()
        self.surf.blit(self.text,
                       ((self.rect.width / 2) - (self.text_rect.width / 2),
                        (self.rect.height / 2) - (self.text_rect.height / 2)))

        # TODO:finish the Goal object, place on game surface complete game when "dropping" the coins off.
    def place_goal(self, goal_pos: tuple):
        self.rect.topleft = goal_pos
        self.text_rect.center = self.rect.center

    def calc_vert_pos(self, parent_height, vert_position) -> int:
        if vert_position == 'top':
            return 0
        elif vert_position == 'bottom':
            return parent_height - self.height
        else:
            print('Bad vert_position arg exiting.')
            sys.exit(1)


class Coin(pygame.sprite.Sprite):

    vector = pygame.math.Vector2
    images = []
    current_image_index = 0

    def __init__(self, color: tuple):
        super().__init__()
        self.color_code = color
        # self.surf = pygame.Surface((10, 10))
        # self.surf.fill(color)
        self.pos = self.vector(0, 0)
        # self.rect = self.surf.get_rect()
        self.images = self.load_coin_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        # self.center = self.rect.center

    def move_coin(self):
        self.rect.center = self.pos

    ## move_to is not used think about removing...
    def move_to(self, pos):
        self.rect.topleft = pos

    def load_coin_images(self) -> list:
        wdir = pathlib.Path().cwd()
        coin_path = wdir.joinpath('coin-images')
        print(str(coin_path))
        imgs = []
        for f in os.listdir(coin_path):
            img = pygame.image.load( coin_path.joinpath(f) )
            imgs.append(img)
        return imgs

    def update_image(self):
        if self.current_image_index == len(self.images) - 1:
            self.current_image_index = 0
        else:
            self.current_image_index += 1
        self.image = self.images[self.current_image_index]
        self.rect = self.image.get_rect()
        self.move_coin()


class Player(pygame.sprite.Sprite):

    vector = pygame.math.Vector2

    def __init__(self, fric, accel, surface_width, surface_height):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.pos = self.vector(surface_width, surface_height)
        self.rect = self.surf.get_rect()
        self.vel = self.vector(0, 0)
        self.acc = self.vector(0, 0)
        self.fric_const = fric
        self.accel_const = accel
        self.parent_width = surface_width
        self.parent_height = surface_height
        self.coin_count = 0

    def move(self):
        self.acc = self.vector(0, 0)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -self.accel_const
        if pressed_keys[K_RIGHT]:
            self.acc.x = self.accel_const
        if pressed_keys[K_UP]:
            self.acc.y = -self.accel_const
        if pressed_keys[K_DOWN]:
            self.acc.y = self.accel_const

        self.acc.x += self.vel.x * self.fric_const
        self.acc.y += self.vel.y * self.fric_const
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # 30 is the width and height of the player square
        if self.pos.x > self.parent_width - 30:
            self.vel.x = 0
            self.pos.x = self.parent_width - 30
        if self.pos.x < 0:
            self.vel.x = 0
            self.pos.x = 0

        if self.pos.y > self.parent_height - 30:
            self.vel.y = 0
            self.pos.y = self.parent_height - 30
        if self.pos.y < 0:
            self.vel.y = 0
            self.pos.y = 0

        self.rect.topleft = self.pos

    def stop(self):
        self.acc.x = 0
        self.acc.y = 0
        self.vel.x = 0
        self.vel.y = 0


class BoundingBox(pygame.sprite.Sprite):
    def __init__(self, bounded_sprite: Goal):
        super().__init__()
        self. pos = bounded_sprite.pos
        self.surf = pygame.Surface((bounded_sprite.width + 40, bounded_sprite.height + 40))
        self.rect = self.surf.get_rect()


class GameRound:
    def __init__(self, coins: list):
        self.coins_in_play = coins
        self.coin_group = pygame.sprite.Group(coins)

    def update_coins_in_play(self, coins: list):
        self.coins_in_play = coins
        self.coin_group.add(coins)
