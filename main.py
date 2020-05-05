import pygame as pg
import random

from settings import *
from sprites import *


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

        # ceiling = Platform(0, 0, WIDTH * 10, 100)
        # self.platform_list.add(ceiling)

        p2 = Platform(WIDTH / 2 - 400, 100, 200, 20)
        p3 = Platform(WIDTH / 2 - 200, HEIGHT * 9 / 10, 100, 20)
        self.platform_list.add(p2)
        self.platform_list.add(p3)

        self.all_sprites.add(p2)
        self.all_sprites.add(p3)
        # self.all_sprites.add(ceiling)

        self.player.collide_list.add(p2)
        self.player.collide_list.add(p3)
        # self.player.collide_list.add(ceiling)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        # self.player.update()
        # self.all_objects.update()

        # self.camera.update()

    def events(self):
        # Game Loop - events

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
