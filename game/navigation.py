from __future__ import annotations

from typing import Optional

import pygame as pg

from drawer import Drawer
from game.settings import *


class NavigatorMeta(type):
    _instance: Optional[Navigator] = None

    def __call__(cls, game) -> Navigator:
        if cls._instance is None:
            cls._instance = super().__call__(game)
        return cls._instance


class Navigator(metaclass=NavigatorMeta):
    def __init__(self, game):
        self.game = game
        self.drawer = Drawer(game.screen)

    def wait_for_key(self, fun=None):
        waiting = True
        while waiting:
            self.game.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.game.running = False
                    pg.quit()
                if event.type == pg.KEYUP and event.key == pg.K_RETURN:
                    waiting = False
                    if fun is not None:
                        fun()

    def show_tutorial_done_screen(self):
        self.__show_screen_with_text_n_finish("You have finished the tutorial!")

    def show_go_screen(self):
        self.__show_screen_with_text_n_finish("GAME OVER")

    def show_congrats_screen(self):
        self.__show_screen_with_text_n_finish("Congratulations, you have won!")

    def __show_screen_with_text_n_finish(self, text):
        self.game.screen.fill(RED)
        self.drawer.draw_text(text, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        pg.display.flip()
        self.wait_for_key(lambda: self.game.stop())

    def go_to_store(self):
        self.game.screen.fill(RED)
        self.game.draw_stats_bar()
        self.drawer.draw_text("Store", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawer.draw_text("Things you can buy: (1) Extra speed: 50g    (2) Extra HP: 50g", 22, WHITE, WIDTH / 2,
                              HEIGHT / 2)
        self.drawer.draw_text("Press Enter to exit store", 22, WHITE, WIDTH / 2, HEIGHT * 5 / 6)
        pg.display.flip()
        waiting = True
        while waiting:
            self.playing = False
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_1:
                    if self.game.player.money >= 50:
                        self.game.player.got_double_speed = True
                        self.game.player.money -= 50
                        self.game.screen.fill(RED, (0, 0, 200, 200))
                        self.drawer.draw_text("Bought double jump - press left shift to activate", 20, WHITE, WIDTH / 2,
                                              HEIGHT * 3 / 4)
                        self.game.draw_stats_bar()
                        pg.display.flip()
                    else:
                        self.drawer.draw_text("Not enough money", 20, WHITE, WIDTH / 2, HEIGHT * 5 / 6 - 100)
                        pg.display.flip()

                if event.type == pg.KEYDOWN and event.key == pg.K_2:
                    if self.game.player.money >= 50:
                        self.game.player.hp += 10
                        self.game.player.money -= 50
                        self.game.screen.fill(RED, (0, 0, 200, 200))
                        self.drawer.draw_text("Bought hp", 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4 - 100)
                        self.game.draw_stats_bar()
                        pg.display.flip()
                    else:
                        self.drawer.draw_text("Not enough money", 20, WHITE, WIDTH / 2, HEIGHT * 5 / 6 - 100)
                        pg.display.flip()

                if (event.type == pg.KEYDOWN) and (event.key == pg.K_RETURN):
                    waiting = False
                    self.game.playing = False
                if event.type == pg.QUIT:
                    waiting = False
                    self.game.playing = False

