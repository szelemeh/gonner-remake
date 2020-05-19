import pygame as pg
from game.settings import *
from sprites.actor import Actor


class Coin(Actor):
    def __init__(self, x, y, image):
        super().__init__(x, y, 15, 15)
        self.rect = pg.Surface((15, 15)).get_rect()
        self.image = pg.image.fromstring(image.tobytes(), image.size, image.mode)
        self.vel_y = 0
        self.vel_x = 0
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.apply_gravity()
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
