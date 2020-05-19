from sprites.actor import Actor
from game.physics_helper import *


class Bullet(Actor):
    def __init__(self, x, y, animation=None):
        super().__init__(x, y, 20, 10, animation)
        self.velocity = 20
        self.reach_length = 200
        self.damage = 5

        self.flying = False
        self.target = None
        self.flying_length = 0

    def fire_at(self, x, y):
        self.flying = True
        self.target = (x, y)

    def __next_step(self):
        step = get_next_step_to(
            (self.rect.x, self.rect.y),
            self.target,
            self.velocity)

        self.vel_x = step[0]
        self.vel_y = step[1]

    def update(self):
        if self.flying_length > self.reach_length:
            self.flying = False
            self.vel_x *= 0.9

        if self.flying:
            self.__next_step()
            self.flying_length += self.velocity
        else:
            self.apply_gravity()

        Actor.update(self)
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
