from sprites.actor import ActorState
from sprites.enemies.enemy import *


class GroundEnemy(Enemy):
    def __init__(self, x, y, width, height, animation, target):
        super().__init__(x, y, width, height, animation, target)

    def get_state(self):
        if self.vel_x > 0:
            return ActorState.MOVING_RIGHT
        else:
            return ActorState.MOVING_LEFT

    def update(self):
        Enemy.apply_gravity(self)
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        Actor.update(self)
