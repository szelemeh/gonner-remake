import pygame as pg

from game.settings import *


class Drawer:
    def __init__(self, screen) -> None:
        self.font_name = pg.font.match_font(FONT_NAME)
        self.screen = screen

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
