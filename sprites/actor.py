import pygame as pg
from enum import Enum
from game.settings import *


class Actor(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, animation=None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.vel_x = 0
        self.vel_y = 0

        self.animation = animation
        self.index = 0
        self.image_vel_countdown = 70

    def apply_gravity(self):
        self.vel_y += GRAVITY
        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = HEIGHT - self.rect.height

    def get_state(self):
        if self.vel_x == 0 and self.vel_y < 2.1*GRAVITY:
            return ActorState.IDLE
        if self.vel_y > 2.1*GRAVITY or self.vel_y < 0:
            if self.vel_x == 0:
                return ActorState.JUMPING_IN_PLACE
            if self.vel_x > 0:
                return ActorState.JUMPING_RIGHT
            else:
                return ActorState.JUMPING_LEFT
        if self.vel_x > 0:
            return ActorState.MOVING_RIGHT
        else:
            return ActorState.MOVING_LEFT

    def update(self):
        if self.animation is not None:
            self.animation.set_state(self.get_state())
            self.image = self.animation.update()


class ActorState(Enum):
    IDLE = 0
    MOVING_LEFT = -2
    MOVING_RIGHT = 2
    JUMPING_LEFT = -3
    JUMPING_RIGHT = 3
    JUMPING_IN_PLACE = 4
    HURT = 5
