import pygame as pg
from settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill(LIGHTBLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

    def jump(self):
        self.velocity.y = -15

    def update(self):
        self.acceleration = vec(0, 0.5)

        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_LEFT]:
            self.acceleration.x = -PLAYER_ACCELERATION
        if keys_pressed[pg.K_RIGHT]:
            self.acceleration.x = PLAYER_ACCELERATION

        # apply friction
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION
        # equations of motion
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration
        # wrap around the sides of the screen
        if self.position.x > WIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = WIDTH

        self.rect.midbottom = self.position


class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, size=TILE_SIZE):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((size, size))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size = size


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = w
        self.height = h


class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.position = vec(WIDTH * 3 / 4, HEIGHT / 2)
        self.velocity = vec(0, 0)
        self.move_right = True
        self.acceleration = vec(0, 0)
        self.count = 0

    def update(self):
        self.acceleration = vec(0, 1)

        if self.count == 200:
            self.move_right = False
        if self.count == 0:
            self.move_right = True

        if self.move_right:
            self.count += 1
        else:
            self.count -= 1

        if self.move_right:
            self.acceleration.x = MOB_ACCELERATION
        else:
            self.acceleration.x = -MOB_ACCELERATION

        # apply friction
        self.acceleration.x += self.velocity.x * MOB_FRICTION
        # equations of motion
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        self.rect.midbottom = self.position
