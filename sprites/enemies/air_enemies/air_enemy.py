from sprites.enemies.enemy import *


class AirEnemy(Enemy):
    def __init__(self, x, y, width, height, images_left, images_right, target):
        super().__init__(x, y, width, height, images_left, images_right, target)

    def update(self):

        Enemy.update(self)
