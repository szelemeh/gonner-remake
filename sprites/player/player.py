from game.settings import *
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

        self.vel_x = 0
        self.vel_y = 0

    def update(self):

        self.apply_gravity()

        self.rect.x += self.vel_x

        block_hit_list = pg.sprite.spritecollide(self, self.collide_list, False)
        for block in block_hit_list:
            if self.vel_x > 0:
                self.rect.right = block.rect.left
            elif self.vel_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.vel_y

        block_hit_list = pg.sprite.spritecollide(self, self.collide_list, False)
        for block in block_hit_list:

            if self.vel_y > 0:
                self.rect.bottom = block.rect.top
            elif self.vel_y < 0:
                self.rect.top = block.rect.bottom

            self.vel_y = 0

    def apply_gravity(self):
        self.vel_y += .35

        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = HEIGHT - self.rect.height


    def jump(self):

        self.rect.y += 2
        platform_hit_list = pg.sprite.spritecollide(self, self.collide_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= HEIGHT:
            self.vel_y = -13

    def go_left(self):
        self.vel_x = -6

    def go_right(self):
        self.vel_x = 6

    def stop(self):
        self.vel_x = 0
