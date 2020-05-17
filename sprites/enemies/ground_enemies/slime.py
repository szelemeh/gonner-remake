from sprites.enemies.ground_enemies.ground_enemy import GroundEnemy


class Slime(GroundEnemy):
    def __init__(self, x, y, width, height, images_left, images_right, target):
        super().__init__(x, y, width, height, images_left, images_right, target)

        self.vel_x = 1

    def move(self):
        difference = self.rect.x - self.target.rect.x
        if difference > 0:
            self.vel_x = -1
        elif difference < 0:
            self.vel_x = 1
        else:
            self.vel_x = 0

    def update(self):

        self.move()

        GroundEnemy.update(self)
