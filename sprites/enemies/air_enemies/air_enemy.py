from sprites.enemies.enemy import *


class AirEnemy(Enemy):
    def __init__(self, x, y, width, height, animation, target):
        super().__init__(x, y, width, height, animation, target)

    def update(self):
        Actor.update(self)
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
