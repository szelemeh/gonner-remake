from random import randint

from sprites.enemies.air_enemies.air_enemy import AirEnemy, Enemy
from sprites.enemies.enemy import get_rand_member_of


class Ghost(AirEnemy):
    def __init__(self, x, y, width, height, ghost_animation, target):
        super().__init__(x, y, width, height, ghost_animation, target)
        self.state_countdown = 0
        self.move_unit = 1
        self.vel_x = 1

    def update(self):
        if self.state_countdown == 0:
            # giving random time
            self.state_countdown = randint(100, 200)
            # choosing random direction (or staying in place)
            self.vel_x = get_rand_member_of([-1, 0, 1])

        self.state_countdown -= 1
        AirEnemy.update(self)
