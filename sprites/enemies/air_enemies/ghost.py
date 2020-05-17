from sprites.enemies.air_enemies.air_enemy import AirEnemy, Enemy


class Ghost(AirEnemy):
    def __init__(self, x, y, width, height, images_left, images_right, target):
        super().__init__(x, y, width, height, images_left, images_right, target)

    def update(self):

        AirEnemy.update(self)
