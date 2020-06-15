from __future__ import annotations

from glob import glob
from random import randint
from typing import Optional

import pygame as pg
from PIL import Image

from drawer import Drawer
from game.settings import *
from sprites.enemies.air_enemies.ghost import Ghost
from sprites.enemies.enemy import EnemyType
from sprites.enemies.ground_enemies.slime_block import SlimeBlock
from sprites.enemies.ground_enemies.worm import Worm
from sprites.player.coin import Coin
from sprites.player.player import Player
from sprites.sprite_animation import SpriteAnimation
from sprites.weapon.bullet import Bullet
from sprites.world.platform import Platform
from sprites.world.tile import Tile


def get_images(path):
    return [Image.open(img) for img in glob(path)]


class CreatorMeta(type):
    _instance: Optional[Creator] = None

    def __call__(cls) -> Creator:
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


class Creator(metaclass=CreatorMeta):
    def __init__(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.player_collide_list = pg.sprite.Group()
        self.shiftable = pg.sprite.Group()
        self.texts = []
        self.player = self.create_player(WIDTH / 3, HEIGHT / 2)

    def create_platform(self, x, y, w, h):
        created_platform = Platform(x, y, w, h)
        self.all_sprites.add(created_platform)
        self.platforms.add(created_platform)
        self.player_collide_list.add(created_platform)
        self.shiftable.add(created_platform)
        return created_platform

    def create_wall(self, x, y, n):
        for i in range(n):
            for j in range(n):
                created_tile = Tile(x + i * TILE_SIZE, y + j * TILE_SIZE)
                self.all_sprites.add(created_tile)
                self.tiles.add(created_tile)
                self.shiftable.add(created_tile)
                self.player_collide_list.add(created_tile)

    def create_gold(self, x, y):
        created_coin = Coin(x, y, Image.open("img/gold/gold_0.png"))
        self.all_sprites.add(created_coin)
        self.shiftable.add(created_coin)
        self.coins.add(created_coin)
        return created_coin

    def create_enemy(self, enemy_type, x, y, target):
        if enemy_type == EnemyType.GHOST:
            animation = SpriteAnimation()
            animation.add_idle(get_images("img/ghost/ghost_normal.png"))
            animation.add_move(get_images("img/ghost/ghost.png"))
            created_enemy = Ghost(x, y, 51, 73, animation, target)

        elif enemy_type == EnemyType.SLIME:
            animation = SpriteAnimation()
            animation.add_idle(get_images("img/slime/walk/slime_walk1.png"))
            animation.add_move(get_images("img/slime/walk/*"))
            created_enemy = Worm(x, y, 63, 23, animation, target)

        elif enemy_type == EnemyType.WORM:
            animation = SpriteAnimation()
            animation.add_idle(get_images("img/worm/walk/worm.png"))
            animation.add_move(get_images("img/worm/walk/*"))
            created_enemy = Worm(x, y, 63, 23, animation, target)

        elif enemy_type == EnemyType.SLIME_BLOCK:
            animation = SpriteAnimation()
            animation.add_idle(get_images("img/slimeblock/slimeBlock.png"))
            animation.add_move(get_images("img/slimeblock/slimeBlock.png"))
            created_enemy = SlimeBlock(x, y, 51, 50, animation, target)

        else:
            return None

        self.all_sprites.add(created_enemy)
        self.shiftable.add(created_enemy)
        self.enemies.add(created_enemy)
        return created_enemy

    def create_player(self, x, y) -> Player:
        animation = SpriteAnimation()
        animation.add_hurt(get_images("img/player/p1_hurt.png"))
        animation.add_idle(get_images("img/player/p1_stand.png"))
        animation.add_move(get_images("img/player/walk/*"))
        animation.add_jump(get_images("img/player/p1_jump.png"))
        created_player = Player(x, y, animation)
        self.all_sprites.add(created_player)
        return created_player

    def create_bullet(self, x, y):
        created_bullet = Bullet(x, y, None)
        self.shiftable.add(created_bullet)
        self.bullets.add(created_bullet)
        self.all_sprites.add(created_bullet)
        return created_bullet

    def empty_all_objects(self):
        self.all_sprites.empty()
        self.platforms.empty()
        self.tiles.empty()
        self.enemies.empty()
        self.coins.empty()
        self.bullets.empty()
        self.player_collide_list.empty()
        self.shiftable.empty()

    def build_level(self, player):

        self.empty_all_objects()
        self.all_sprites.add(player)
        player.stop()

        self.right_wall = self.create_platform(WIDTH * 4, 0, 120, HEIGHT)

        maps = ["levels/map_1.txt", "levels/map_2.txt", "levels/map_3.txt", \
                "levels/map_4.txt", "levels/map_5.txt", "levels/map_6.txt", "levels/map_7.txt", \
                "levels/map_8.txt", "levels/map_10.txt", "levels/map_9.txt"]

        rand = randint(0, 9)

        level_map = self.read_map(maps[rand])

        self.build_map(level_map)

    def build_level_final(self, player):

        self.empty_all_objects()
        self.all_sprites.add(player)

        player.stop()

        self.right_wall = self.create_platform(WIDTH * 4, 0, 120, HEIGHT)

        level_map = self.read_map('levels/map_final.txt')

        self.build_map(level_map)

        self.boss = self.create_enemy(EnemyType.SLIME_BLOCK, WIDTH * 2,
                                      HEIGHT / 2, player)

    def reset_level(self, player):
        self.empty_all_objects()
        self.all_sprites.add(player)
        player.stop()
        self.right_wall = self.create_platform(WIDTH * 5, 0, 120, HEIGHT * 10)

    def build_tutorial_level(self, player, screen):
        self.reset_level(player)

        level_map = self.read_map('levels/map_tutorial.txt')

        self.player = player
        self.drawer = Drawer(screen)

        self.build_map(level_map)

    def build_map(self, level_map):
        """ Reads map in txt format """
        for row, objs in enumerate(level_map):
            for col, obj in enumerate(objs):
                self.create_object(row, col, obj)

    def create_object(self, row, col, obj):
        """ Creates tiles, enemies and coins, also text for tutorial level """
        if obj == '1':
            self.create_wall(col * TILE_SIZE, row * TILE_SIZE, 1)
        elif obj == 'm':
            self.create_text(self.drawer, col * TILE_SIZE, row * TILE_SIZE,
                             "Move left or right using arrows <- and ->!")
        elif obj == 'j':
            self.create_text(self.drawer, col * TILE_SIZE, row * TILE_SIZE,
                             "Jump using 'up' arrow!")
        elif obj == 'c':
            self.create_text(self.drawer, col * TILE_SIZE, row * TILE_SIZE,
                             "Collect coins!")
            self.create_gold(col * TILE_SIZE, (row + 2) * TILE_SIZE)
        elif obj == 'C':
            self.create_gold(col * TILE_SIZE, (row - 2) * TILE_SIZE)
        elif obj == 'w':
            self.create_text(self.drawer, col * TILE_SIZE, row * TILE_SIZE,
                             "Climb a wall by coming closer to it!")
        elif obj == 's':
            self.create_text(self.drawer, col * TILE_SIZE, row * TILE_SIZE,
                             "Press space to shoot!")
        elif obj == 'G':
            self.create_enemy(EnemyType.GHOST, col * TILE_SIZE,
                              row * TILE_SIZE, self.player)
        elif obj == 'd':
            self.create_text(self.drawer, col * TILE_SIZE, row * TILE_SIZE,
                             "Press 'shift' to enable double speed!")
        elif obj == 'S':
            self.create_enemy(EnemyType.SLIME, col * TILE_SIZE,
                              row * TILE_SIZE, self.player)
        elif obj == 'W':
            self.create_enemy(EnemyType.WORM, col * TILE_SIZE, row * TILE_SIZE,
                              self.player)

    @staticmethod
    def read_map(path):
        level_map = []
        with open(path, 'r') as f:
            for line in f:
                level_map.append(line)
        return level_map

    def create_text(self, drawer, x, y, text):
        text_surface = drawer.draw_medium_text(text, x, y)
        self.texts.append(text_surface)
