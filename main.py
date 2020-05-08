import pygame as pg
import random

from settings import *
from sprites import *
from enemies import *


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.world_shift = 0
        self.can_jump = True

    def create_wall(self, x, y, n):
        for i in range(n):
            for j in range(n):
                tile = Tile(x + i * TILE_SIZE, y + j * TILE_SIZE)
                self.all_sprites.add(tile)
                self.tiles_list.add(tile)
                self.player.collide_list.add(tile)

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        self.all_objects = pg.sprite.Group()
        self.platform_list = pg.sprite.Group()
        self.tiles_list = pg.sprite.Group()
        self.enemy_list = pg.sprite.Group()

        # self.create_wall(WIDTH / 2, HEIGHT / 2, 2)

        self.player = Player()
        self.all_sprites.add(self.player)

        self.worm = Worm(WIDTH / 3, HEIGHT / 2, 63, 23, self.player)
        self.slime = Slime(WIDTH / 3, HEIGHT / 2, 63, 23, self.player)
        self.ghost = Ghost(WIDTH / 3, HEIGHT / 2, 63, 23, self.player)

        self.enemy_list.add(self.worm)
        self.enemy_list.add(self.ghost)
        self.enemy_list.add(self.slime)
        self.all_sprites.add(self.worm)
        self.all_sprites.add(self.slime)
        self.all_sprites.add(self.ghost)

        self.right_wall = Platform(WIDTH * 4, 0, 120, HEIGHT)
        self.platform_list.add(self.right_wall)
        self.all_sprites.add(self.right_wall)
        self.player.collide_list.add(self.right_wall)


        p2 = Platform(WIDTH / 2 - 400, 100, 200, 20)
        p3 = Platform(WIDTH / 2 - 200, HEIGHT * 9 / 10, 100, 20)
        self.platform_list.add(p2)
        self.platform_list.add(p3)

        self.all_sprites.add(p2)
        self.all_sprites.add(p3)

        self.player.collide_list.add(p2)
        self.player.collide_list.add(p3)

        self.create_wall(room[0][8][0], room[0][8][1] + TILE_SIZE * 2, 2)
        
        self.create_wall(room[1][1][2], room[1][1][3], 4)
        self.create_wall(room[1][3][2], room[1][3][3], 2)

        self.create_wall(room[2][0][2], room[2][0][3], 4)
        self.create_wall(room[2][0][2], room[2][0][3], 4)

        self.create_wall(room[3][0][2], room[3][0][3], 3) 
        self.create_wall(room[3][1][2], room[3][1][3], 1)
        self.create_wall(room[3][7][2], room[3][7][3], 4)

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):

        for enemy in self.enemy_list:
            if abs(enemy.rect.x - self.player.rect.x) == self.player.rect.width / 2 and self.player.rect.bottom == enemy.rect.bottom:
                self.player.kill()

        self.all_sprites.update()
        self.worm.update()

    def events(self):
        # Game Loop - events

        go_right = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.go_left()
                if event.key == pg.K_RIGHT:
                    self.player.go_right()
                    go_right = True
                if event.key == pg.K_UP:
                    self.player.jump()

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pg.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()

        self.all_sprites.update()

        if self.player.rect.right >= 500:
            diff = self.player.rect.right - 500
            self.player.rect.right = 500
            self.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if self.player.rect.left <= 120:
            diff = 120 - self.player.rect.left
            self.player.rect.left = 120
            self.shift_world(diff)


        #current_position = self.player.rect.x + self.world_shift
        
        if( abs( (self.right_wall.rect.x - self.right_wall.rect.width / 2) - (self.player.rect.x + self.player.rect.width / 2)) == self.player.rect.width):
            self.playing = False
            self.running = False

    
    def draw(self):

        # Draw the background
        self.screen.fill(RED)

        # Draw all the sprite lists that we have
        # self.player_sprite.draw(self.screen)
        # self.all_objects.draw(self.screen)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        pass  # here there will be game start screen

    def show_go_screen(self):
        pass  # here there will be end game screen

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for tile in self.tiles_list:
            tile.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
