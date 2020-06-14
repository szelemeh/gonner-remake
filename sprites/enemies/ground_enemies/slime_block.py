from game.physics_helper import get_next_step_to
from sprites.enemies.ground_enemies.ground_enemy import GroundEnemy


class SlimeBlock(GroundEnemy):
    def __init__(self, x, y, width, height, slime_animation, target):
        super().__init__(x, y, width, height, slime_animation, target)

        self.attack_velocity = 3
        self.move_countdown = 100
        self.vel_x = 2
        self.max_hp = 50
        self.hp = 50

    def attack(self):
        velocity = get_next_step_to(
            (self.rect.x, self.rect.y),
            (self.target.rect.x, self.target.rect.y),
            self.attack_velocity)
        self.vel_x = velocity[0]
        self.vel_y = velocity[1]

    def alive(self):
        return self.hp > 0

    def rest(self):
        difference = self.rect.x - self.target.rect.x
        if difference > 0:
            self.vel_x = -3
        elif difference < 0:
            self.vel_x = 3
        else:
            self.vel_x = 0

    def update(self):
        if 300 > self.get_target_distance() > 30:
            self.attack()
        else:
            self.rest()

        GroundEnemy.update(self)
