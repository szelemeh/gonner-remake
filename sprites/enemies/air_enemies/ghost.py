from sprites.enemies.air_enemies.air_enemy import AirEnemy, Enemy


class Ghost(AirEnemy):
    def __init__(self, x, y, width, height, target):
        super().__init__(x, y, width, height, target)

        Enemy.load_images(self, '../../../img/ghost/ghost.png')

    def update(self):

        AirEnemy.update(self)
