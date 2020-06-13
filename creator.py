
from __future__ import annotations

from random import randint

from glob import glob
from typing import Optional

from PIL import Image
import pygame as pg
from game.settings import *
from sprites.weapon.bullet import Bullet
from sprites.enemies.air_enemies.ghost import Ghost
from sprites.enemies.enemy import EnemyType
from sprites.enemies.ground_enemies.slime_block import SlimeBlock
from sprites.enemies.ground_enemies.worm import Worm
from sprites.player.coin import Coin
from sprites.player.player import Player
from sprites.sprite_animation import SpriteAnimation
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


    def build_level(self, number, player):

        self.empty_all_objects()
        self.all_sprites.add(player)
        player.stop()

        for i in range(1, 5):
            self.create_enemy(EnemyType.WORM, WIDTH * i / 3, HEIGHT / 2, player)
            self.create_enemy(EnemyType.SLIME, WIDTH * i - 50, HEIGHT - 50, player)
            self.create_enemy(EnemyType.GHOST, WIDTH * i - 50, HEIGHT / 2, player)


        self.create_gold(WIDTH / 2, HEIGHT / 2)
        self.create_gold(WIDTH * 2, HEIGHT / 2)
        self.create_gold(WIDTH * 3, HEIGHT / 2)

        self.right_wall = self.create_platform(WIDTH * 4, 0, 120, HEIGHT)

        maps = ["levels/map_1.txt", "levels/map_2.txt", "levels/map_3.txt", \
            "levels/map_4.txt", "levels/map_5.txt", "levels/map_6.txt", "levels/map_7.txt", \
                "levels/map_8.txt", "levels/map_10.txt", "levels/map_9.txt" ]
        
        rand = randint(0, 1)

        map = []
        with open(maps[rand], 'r') as f:
            for line in f:
                map.append(line)

        for row, tiles in enumerate(map):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    self.create_wall(col * TILE_SIZE, row * TILE_SIZE, 1)



    def build_level_final(self, player):

        self.empty_all_objects()
        self.all_sprites.add(player)

        player.stop()

        self.right_wall = self.create_platform(WIDTH * 4, 0, 120, HEIGHT)

        map = []
        with open('levels/map_final.txt', 'r') as f:
            for line in f:
                map.append(line)

        for row, tiles in enumerate(map):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    self.create_wall(col * TILE_SIZE, row * TILE_SIZE, 1)

        self.boss = self.create_enemy(EnemyType.SLIME_BLOCK, WIDTH / 2, HEIGHT / 2, player)
