from game.settings import *
import pygame as pg

from sprites.actor import Actor


class Player(Actor):

    def __init__(self, x, y, player_animation):
        super().__init__(x, y, 67, 95, player_animation)

        self.collide_list = pg.sprite.Group()

        self.hp = PLAYER_MAX_HP
        self.money = 0
        self.got_double_speed = False

        self.weapon = None

        self.damage_countdown = 10

    def fire(self):
        if self.weapon is not None:
            self.weapon.fire_from_at_direction(
                self.rect.x,
                self.rect.y + 47,
                self.animation.get_direction())

    def update(self):

        self.apply_gravity()

        self.rect.x += self.vel_x

        block_hit_list = pg.sprite.spritecollide(self, self.collide_list, False)
        if len(block_hit_list) > 0:
            self.vel_y = -1
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

        Actor.update(self)

    def receive_damage(self, amount):
        if self.damage_countdown == 0:
            self.hp -= amount
            self.damage_countdown = 10
        self.damage_countdown -= 1

    def jump(self):

        self.rect.y += 2
        platform_hit_list = pg.sprite.spritecollide(self, self.collide_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0:
            self.vel_y = -13

        self.rect.x += 2
        platform_hit_list = pg.sprite.spritecollide(self, self.collide_list, False)
        self.rect.x -= 2

        if len(platform_hit_list) > 0:
            self.vel_y = -13

        self.rect.x -= 2
        platform_hit_list = pg.sprite.spritecollide(self, self.collide_list, False)
        self.rect.x += 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= HEIGHT:
            self.vel_y = -13

    def go_left(self):
        self.vel_x = -6

    def go_left_fast(self):
        self.vel_x = -12

    def go_right(self):
        self.vel_x = 6

    def go_right_fast(self):
        self.vel_x = 12

    def stop(self):
        self.vel_x = 0
