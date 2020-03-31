# Gonner - platform game remake

import pygame as pg
import pymunk as pm
import random
from settings import *
from sprites import *
from pymunk import Vec2d


class Game:
    def __init__(self):
        # initialize game window, etc
        self.running = True
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.mixer.init()
        pg.init()

        # Pymunk stuff.
        self.space = pm.Space()
        self.space.gravity = Vec2d(0.0, -900.0)

    def new(self):
        # start a new game
        self.space = pm.Space()
        self.space.gravity = (0, -1000)

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        self.player = Player(self, self.space)
        self.all_sprites.add(self.player)

        p1 = Platform(0, HEIGHT-40, WIDTH, 40, self.space)
        self.all_sprites.add(p1)
        self.platforms.add(p1)

        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

    def update(self):
        # Game loop - Update
        self.space.step(1/60)  # Update physics.
        self.all_sprites.update()

    def handle_events(self):
        # Game loop - events
        for event in pg.event.get():
            # check for closing the window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
