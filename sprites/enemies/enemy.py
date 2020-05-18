from math import sqrt
from random import randint
from enum import Enum
from sprites.actor import Actor


def get_rand_member_of(members):
    i = randint(0, len(members) - 1)
    return members[i]


def get_distance_between(x1, y1, x2, y2):
    distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance


class Enemy(Actor):

    def __init__(self, x, y, width, height, animation, target):
        super().__init__(x, y, width, height, animation)
        self.target = target

    def get_target_distance(self):
        t_x = self.target.rect.x
        t_y = self.target.rect.y
        s_x = self.rect.x
        s_y = self.rect.y
        return get_distance_between(t_x, t_y, s_x, s_y)


class EnemyType(Enum):
    # Air enemies
    GHOST = 1
    # Ground enemies
    WORM = 2,
    SLIME = 3
