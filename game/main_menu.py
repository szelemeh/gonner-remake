import sys
from enum import Enum

import pygame as pg

from game.drawer import Drawer
from game.game import Game
from game.navigation import Navigator
from game.settings import *


class MainMenu:
    def __init__(self):
        self.game = Game()
        self.drawer = Drawer(self.game.screen)
        self.nav = Navigator(self.game)
        self.levels = 3

    def show(self):
        self.game.screen.fill(RED)
        self.drawer.draw_text("Gonner", 48, WHITE, WIDTH / 2, HEIGHT / 10)
        self.drawer.draw_text("Play - press 1", 48, WHITE, WIDTH / 2, 3 * HEIGHT / 10)
        self.drawer.draw_text("Tutorial - press 2", 48, WHITE, WIDTH / 2, 4 * HEIGHT / 10)
        self.drawer.draw_text("Quit - press 3", 48, WHITE, WIDTH / 2, 5 * HEIGHT / 10)
        pg.display.flip()
        self.__run_menu_loop()

    def __run_menu_loop(self):
        waiting = True
        while waiting:
            self.playing = False
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        waiting = False
                        self.play()
                    elif event.key == pg.K_2:
                        waiting = False
                        self.tutorial()
                    elif event.key == pg.K_3:
                        waiting = False
                        self.quit()
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

    def play(self):
        self.game.reset()
        for lvl in range(self.game.number_of_levels):
            if self.game.running:
                print("You're on ", lvl)
                self.game.new(lvl)
        # show congratulation screen or game over screen
        self.show()

    def tutorial(self):
        self.game.screen.fill(RED)
        self.drawer.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawer.draw_text("Use arrows to move around and space to shoot", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawer.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.nav.wait_for_key()

    def quit(self):
        pg.quit()


class Item(Enum):
    PLAY = 0,
    TUTORIAL = 1,
    QUIT = 2
