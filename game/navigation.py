from __future__ import annotations

import pygame as pg
from game.settings import *

from typing import Optional


class NavigatorMeta(type):

    _instance: Optional[Navigator] = None

    def __call__(cls) -> Navigator:
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


class Navigator(metaclass=NavigatorMeta):
    def __init__(self):
        self.font_name = pg.font.match_font(FONT_NAME)

    def set_game(self, game):
        self.game = game

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.game.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.game.running = False
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.game.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        self.game.screen.fill(RED)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use arrows to move and jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # if not self.game.running:
        #     return
        self.game.screen.fill(RED)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        pg.display.flip()
        self.wait_for_key()

    def go_to_store(self):
        self.game.screen.fill(RED)
        self.game.draw_stats_bar()
        self.draw_text("Store", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Things you can buy: (1) Extra speed: 50g    (2) Extra HP: 50g", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press Enter to exit store", 22, WHITE, WIDTH / 2, HEIGHT * 5 / 6)
        pg.display.flip()
        waiting = True
        while waiting:
            self.playing = False
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_1:
                    if self.game.player.money >= 50:
                        print("bought speed")
                        self.game.player.got_double_speed = True
                        self.game.player.money -= 50
                        self.game.screen.fill(RED, (0, 0, 200, 200))
                        self.game.draw_stats_bar()
                        pg.display.flip()
                    else:
                        self.game.draw_text("Not enough money", 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
                        pg.display.flip()

                if event.type == pg.KEYDOWN and event.key == pg.K_2:
                    if self.game.player.money >= 50:
                        print("bought hp")
                        self.game.player.hp += 500
                        self.game.player.money -= 50
                        self.game.screen.fill(RED, (0, 0, 200, 200))
                        self.game.draw_stats_bar()
                        pg.display.flip()
                    else:
                        self.game.draw_text("Not enough money", 20, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
                        pg.display.flip()

                if (event.type == pg.KEYDOWN) and (event.key == pg.K_RETURN):
                    waiting = False
                    self.game.playing = False
                    # self.go_to_next_level()
                if event.type == pg.QUIT:
                    waiting = False
                    self.game.playing = False

    def go_to_next_level(self, number):
        pass
