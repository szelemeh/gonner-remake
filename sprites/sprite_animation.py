from PIL import ImageOps

from sprites.actor import *
from sprites.weapon.direction import Direction


def mirror(pil_images):
    mirrored = []
    for img in pil_images:
        mirrored.append(ImageOps.mirror(img))
    return mirrored


def convert_to_pg_image(pil_images):
    pg_images = []
    for img in pil_images:
        pg_images.append(pg.image.fromstring(img.tobytes(), img.size, img.mode))
    return pg_images


class SpriteAnimation:
    def __init__(self):
        self.current_images = None
        self.image_change_countdown = 1
        self.index = 0
        self.move_left = None
        self.move_right = None
        self.idle_left = None
        self.idle_right = None
        self.jump_left = None
        self.jump_right = None
        self.hurt_left = None
        self.hurt_right = None

    def add_move(self, images):
        self.move_left = convert_to_pg_image(mirror(images))
        self.move_right = convert_to_pg_image(images)

    def add_jump(self, images):
        self.jump_left = convert_to_pg_image(mirror(images))
        self.jump_right = convert_to_pg_image(images)

    def add_idle(self, images):
        self.idle_left = convert_to_pg_image(mirror(images))
        self.idle_right = convert_to_pg_image(images)

    def add_hurt(self, images):
        self.hurt_left = convert_to_pg_image(mirror(images))
        self.hurt_right = convert_to_pg_image(images)

    def set_state(self, entity_state):
        if entity_state == ActorState.IDLE:
            if self.current_images in [self.move_left, self.jump_left, self.idle_left]:
                self.current_images = self.idle_left
            else:
                self.current_images = self.idle_right

        elif entity_state == ActorState.MOVING_LEFT:
            self.current_images = self.move_left

        elif entity_state == ActorState.MOVING_RIGHT:
            self.current_images = self.move_right

        elif entity_state == ActorState.FLYING_LEFT:
            self.current_images = self.jump_left

        elif entity_state == ActorState.FLYING_RIGHT:
            self.current_images = self.jump_right

        elif entity_state == ActorState.FLYING_IN_PLACE:
            if self.current_images in [self.move_left, self.jump_left, self.idle_left]:
                self.current_images = self.jump_left
            else:
                self.current_images = self.jump_right
        elif entity_state == ActorState.HURT:
            if self.current_images in [self.move_left, self.jump_left, self.idle_left]:
                self.current_images = self.hurt_left
            else:
                self.current_images = self.hurt_right

    def get_direction(self) -> Direction:
        if self.current_images in [self.move_left, self.jump_left, self.idle_left]:
            return Direction.WEST
        else:
            return Direction.EAST

    def update(self):
        if self.image_change_countdown == 0:
            self.index += 1
            self.image_change_countdown = 10
        self.image_change_countdown -= 1

        if self.index >= len(self.current_images):
            self.index = 0
        self.image = self.current_images[self.index]
        return self.image
