import pygame as pg

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
