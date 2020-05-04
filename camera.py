import pygame as pg
import random
from settings import *
from sprites import *


class Camera:
    def __init__(self, platforms, mobs, player):
        self.platforms = platforms
        self.player = player
        self.mobs = mobs

    def update(self):
        # if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.position.y += abs(self.player.velocity.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.velocity.y)
            for mob in self.mobs:
                mob.position.y += abs(self.player.velocity.y)

        # if player reaches bottom 1/4 of screen
        if self.player.rect.bottom >= HEIGHT * 3 / 4:
            self.player.position.y -= abs(self.player.velocity.y)
            for plat in self.platforms:
                plat.rect.y -= abs(self.player.velocity.y)
            for mob in self.mobs:
                mob.position.y -= abs(self.player.velocity.y)

        # if player reaches right 1/4 of screen
        if self.player.rect.right >= WIDTH * 3 / 4:
            self.player.position.x -= max(abs(self.player.velocity.x), 2)
            for plat in self.platforms:
                plat.rect.right -= max(abs(self.player.velocity.x), 2)
            for mob in self.mobs:
                mob.position.x -= max(abs(self.player.velocity.x), 2)

        # if player reaches left 1/4 of screen
        if self.player.rect.left <= WIDTH / 4:
            self.player.position.x += max(abs(self.player.velocity.x), 2)
            for plat in self.platforms:
                plat.rect.right += max(abs(self.player.velocity.x), 2)
            for mob in self.mobs:
                mob.position.x += max(abs(self.player.velocity.x), 2)
