from sprites.weapon.direction import Direction


class Weapon:
    def __init__(self, creator):
        self.bullet_creator = creator

    def fire_from_at_direction(self, x, y, direction):
        bullet = self.bullet_creator.create_bullet(x, y)

        if direction == Direction.WEST:
            bullet.fire_at(x - 100000, y)
        elif direction == Direction.EAST:
            bullet.fire_at(x + 100000, y)
