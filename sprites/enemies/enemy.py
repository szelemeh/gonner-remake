from math import sqrt
from random import randint
from enum import Enum

from game.physics_helper import get_distance_between
from sprites.actor import Actor


def get_rand_member_of(members):
    i = randint(0, len(members) - 1)
    return members[i]


class Enemy(Actor):

    def __init__(self, x, y, width, height, animation, target):
        super().__init__(x, y, width, height, animation)
        self.target = target
        self.hp = 10

    def get_target_distance(self):
        t_x = self.target.rect.x
        t_y = self.target.rect.y
        s_x = self.rect.x
        s_y = self.rect.y
        return get_distance_between(t_x, t_y, s_x, s_y)

    def update(self):
        if self.hp <= 0:
            self.kill()
        Actor.update(self)


class EnemyType(Enum):
    # Air enemies
    GHOST = 1
    # Ground enemies
    WORM = 2,
    SLIME = 3
    # Bosses
    SLIME_BLOCK = 4
