import pygame as pg
from main.settings import *


class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, size=TILE_SIZE):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((size, size))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size = size
