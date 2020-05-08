from sprites.enemies.enemy import *


class AirEnemy(Enemy):
    def __init__(self, x, y, width, height, target):
        super().__init__(x, y, width, height, target)

    def update(self):

        Enemy.update(self)
