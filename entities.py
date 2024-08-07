## Enity classes
import pygame
from pygame.locals import *

class coin(pygame.sprite.Sprite):

    vector = pygame.math.Vector2

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 255, 30))
        self.pos = self.vector(0, 0)
        self.rect = self.surf.get_rect(center = self.pos)

    def move(self):
        self.rect = self.surf.get_rect(center = self.pos)

class player(pygame.sprite.Sprite):

    vector = pygame.math.Vector2

    def __init__(self, fric, accel, surface_width, surface_height):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect(center = (10, 420))


        self.pos = self.vector((10, 385))
        self.vel = self.vector(0, 0)
        self.acc = self.vector(0, 0)
        self.fric_const = fric
        self.accel_const = accel
        self.parent_width = surface_width
        self.parent_height = surface_height

    def move(self):
        self.acc = self.vector(0, 0)

        pressesd_keys = pygame.key.get_pressed()

        if pressesd_keys[K_LEFT]:
            self.acc.x = -self.accel_const
        if pressesd_keys[K_RIGHT]:
            self.acc.x = self.accel_const
        if pressesd_keys[K_UP]:
            self.acc.y = -self.accel_const
        if pressesd_keys[K_DOWN]:
            self.acc.y = self.accel_const


        self.acc.x += self.vel.x * self.fric_const
        self.acc.y += self.vel.y * self.fric_const
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > self.parent_width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.parent_width

        if self.pos.y > self.parent_height:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = self.parent_height

        self.rect.midbottom = self.pos


