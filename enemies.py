import pygame as pg
from math import sqrt
from random import randint
import glob
from settings import *
from enemy_state import EnemyState


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


class GroundEnemy(Enemy):
    def __init__(self, x, y, width, height, target):
        super().__init__(x, y, width, height, target)

    def update(self):
        if self.vel_x > 0:
            self.images = self.images_right
        else:
            self.images = self.images_left

        Enemy.apply_gravity(self)

        Enemy.update(self)


class AirEnemy(Enemy):
    def __init__(self, x, y, width, height, target):
        super().__init__(x, y, width, height, target)

    def update(self):

        Enemy.update(self)


class Ghost(AirEnemy):
    def __init__(self, x, y, width, height, target):
        super().__init__(x, y, width, height, target)

        Enemy.load_images(self, 'img/ghost/ghost.png')

    def update(self):

        AirEnemy.update(self)


class Worm(GroundEnemy):
    def __init__(self, x, y, width, height, target):
        super().__init__(x, y, width, height, target)

        self.path = [0, 200]
        self.state_countdown = 0
        self.move_unit = 1
        self.vel_x = 1

        Enemy.load_images(self, 'img/worm/left/*', 'img/worm/right/*')

    def update(self):

        if self.state_countdown == 0:
            # giving random time
            self.state_countdown = randint(180, 360)
            # choosing random direction (or staying in place)
            self.vel_x = get_rand_member_of([-1, 0, 1])

        self.state_countdown -= 1

        GroundEnemy.update(self)


class Slime(GroundEnemy):
    def __init__(self, x, y, width, height, target):
        super().__init__(x, y, width, height, target)

        self.vel_x = 1

        Enemy.load_images(self, 'img/slime/left/*', 'img/slime/right/*')

    def move(self):
        difference = self.rect.x - self.target.rect.x
        if difference > 0:
            self.vel_x = -1
        elif difference < 0:
            self.vel_x = 1
        else:
            self.vel_x = 0

    def update(self):

        self.move()

        GroundEnemy.update(self)



