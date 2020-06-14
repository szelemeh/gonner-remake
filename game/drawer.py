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
        return text_surface, text_rect

    def draw_medium_text(self, text, x, y):
        return self.draw_text(text, 24, WHITE, x, y)

    def draw_player_stats(self, player):
        stats = "Coins: " + str(player.money) + "   HP: "
        self.draw_text(stats, 20, WHITE, 80, 20)
        if player.got_double_speed:
            features = "You've got double speed!"
            self.draw_text(features, 20, WHITE, 120, 40)
        self.draw_health_bar(player, 160, 20, 5)

    def draw_health_bar(self, actor, x, y, size):
        if actor.alive():
            maximal = pg.Surface((actor.max_hp * size, 30))
            maximal.fill(GREY)
            self.draw_surface(maximal, x, y)
            current = pg.Surface((actor.hp * size, 30))
            current.fill(GREEN)
            self.draw_surface(current, x, y)

    def draw_surface(self, surface, x, y):
        rect = surface.get_rect()
        rect.topleft = (x, y)
        self.screen.blit(surface, rect)
