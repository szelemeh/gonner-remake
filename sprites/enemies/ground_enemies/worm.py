from sprites.enemies.ground_enemies.groundenemy import GroundEnemy, Enemy, randint, get_rand_member_of


class Worm(GroundEnemy):
    def __init__(self, x, y, width, height, target):
        super().__init__(x, y, width, height, target)

        self.path = [0, 200]
        self.state_countdown = 0
        self.move_unit = 1
        self.vel_x = 1

        Enemy.load_images(self, 'img/worm/left/*', 'img/worm/right/*')

    def update(self):

        if self.state_countdown == 0:
            # giving random time
            self.state_countdown = randint(180, 360)
            # choosing random direction (or staying in place)
            self.vel_x = get_rand_member_of([-1, 0, 1])

        self.state_countdown -= 1

        GroundEnemy.update(self)
