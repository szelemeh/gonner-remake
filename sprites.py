import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
  
        width = 40
        height = 60
        self.image = pg.Surface((width, height))
        self.image.fill(LIGHTBLUE)
        self.collide_list = pg.sprite.Group()

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

 
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pg.sprite.spritecollide(self, self.collide_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pg.sprite.spritecollide(self, self.collide_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pg.sprite.spritecollide(self, self.collide_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 

class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, size=TILE_SIZE):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((size, size))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size = size


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = w
        self.height = h


class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        #self.position = vec(WIDTH * 3 / 4, HEIGHT / 2)
        #self.velocity = vec(0, 0)
        self.move_right = True
        #self.acceleration = vec(0, 0)
        self.count = 0

    def update(self):
        #self.acceleration = vec(0, 1)

        if self.count == 200:
            self.move_right = False
        if self.count == 0:
            self.move_right = True

        if self.move_right:
            self.count += 1
        else:
            self.count -= 1

        #if self.move_right:
            #self.acceleration.x = MOB_ACCELERATION
        #else:
            #self.acceleration.x = -MOB_ACCELERATION

        # apply friction
        #self.acceleration.x += self.velocity.x * MOB_FRICTION
        # equations of motion
        #self.velocity += self.acceleration
        #self.position += self.velocity + 0.5 * self.acceleration

        #self.rect.midbottom = self.position