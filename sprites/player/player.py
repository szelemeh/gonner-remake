from main.settings import *
import pygame as pg


class Player(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        width = 40
        height = 60
        self.image = pg.Surface((width, height))
        self.image.fill(LIGHTBLUE)
        self.collide_list = pg.sprite.Group()

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

    def update(self):

        self.calc_grav()

        self.rect.x += self.change_x

        block_hit_list = pg.sprite.spritecollide(self, self.collide_list, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = pg.sprite.spritecollide(self, self.collide_list, False)
        for block in block_hit_list:

            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        if self.rect.y >= HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = HEIGHT - self.rect.height

    def jump(self):

        self.rect.y += 2
        platform_hit_list = pg.sprite.spritecollide(self, self.collide_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= HEIGHT:
            self.change_y = -13

    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0
