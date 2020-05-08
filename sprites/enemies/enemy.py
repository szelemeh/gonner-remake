import pygame as pg
from math import sqrt
from random import randint
import glob
from main.settings import *


def get_rand_member_of(members):
    i = randint(0, len(members)-1)
    return members[i]


def get_distance_between(x1, y1, x2, y2):
    distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance


class Enemy(pg.sprite.Sprite):

    def __init__(self, x, y, width, height, target):
        super().__init__()

        self.image = pg.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.vel_x = 0
        self.vel_y = 0

        self.target = target

    def apply_gravity(self):
        self.vel_y += .35

        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = HEIGHT - self.rect.height

    def load_images(self, left, right=''):
        if right == '':
            right = left
        self.index = 0
        self.images_left = [pg.image.load(img) for img in glob.glob(left)]
        self.images_right = [pg.image.load(img) for img in glob.glob(right)]
        self.images = self.images_left
        self.image_change_countdown = 70

    def update(self):

        if self.image_change_countdown == 0:
            self.index += 1
            self.image_change_countdown = 70
        self.image_change_countdown -= 1

        if self.index >= len(self.images):
            self.index = 0
        if self.vel_x != 0:
            self.image = self.images[self.index]

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def get_target_distance(self):
        t_x = self.target.rect.x
        t_y = self.target.rect.y
        s_x = self.rect.x
        s_y = self.rect.y
        return get_distance_between(t_x, t_y, s_x, s_y)
