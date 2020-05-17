from sprites.enemies.enemy import Enemy
from sprites.enemies.ground_enemies.ground_enemy import GroundEnemy
import pygame as pg
from glob import glob

class Slime(GroundEnemy):
    def __init__(self, x, y, width, height, target):
        super().__init__(x, y, width, height, target)

        self.vel_x = 1

        # Enemy.load_images(self, '../../img/slime/left/*', '../../img/slime/right/*')

        right = '../../../img/slime/right/*'
        left = '../../../img/slime/left/*'
        self.index = 0
        self.images_left = [pg.image.load(img) for img in glob(left)]
        self.images_right = [pg.image.load(img) for img in glob(right)]

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
