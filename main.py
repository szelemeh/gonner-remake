from glob import glob
from random import randint

import pygame as pg
from PIL import Image

from game.settings import *
from game.navigation import Navigator
from sprites.enemies.air_enemies.ghost import Ghost
from sprites.enemies.enemy import EnemyType
from sprites.enemies.ground_enemies.slime_block import SlimeBlock
from sprites.enemies.ground_enemies.worm import Worm
from sprites.player.gold import Gold
from sprites.player.player import Player
from sprites.sprite_animation import SpriteAnimation
from sprites.world.platform import Platform
from sprites.world.tile import Tile


def create_player(x, y) -> Player:
    animation = SpriteAnimation()
    animation.add_hurt(get_images("img/player/p1_hurt.png"))
    animation.add_idle(get_images("img/player/p1_stand.png"))
    animation.add_move(get_images("img/player/walk/*"))
    animation.add_jump(get_images("img/player/p1_jump.png"))
    return Player(x, y, animation)


def create_enemy(enemy_type, x, y, target):
    if enemy_type == EnemyType.GHOST:
        animation = SpriteAnimation()
        animation.add_idle(get_images("img/ghost/ghost_normal.png"))
        animation.add_move(get_images("img/ghost/ghost.png"))
        return Ghost(x, y, 51, 73, animation, target)

    elif enemy_type == EnemyType.SLIME:
        animation = SpriteAnimation()
        animation.add_idle(get_images("img/slime/walk/slime_walk1.png"))
        animation.add_move(get_images("img/slime/walk/*"))
        return Worm(x, y, 63, 23, animation, target)
    elif enemy_type == EnemyType.WORM:
        animation = SpriteAnimation()
        animation.add_idle(get_images("img/worm/walk/worm.png"))
        animation.add_move(get_images("img/worm/walk/*"))
        return Worm(x, y, 63, 23, animation, target)


def create_gold(x, y):
    return Gold(x, y, Image.open("img/gold/gold_0.png"))


def get_images(path):
    return [Image.open(img) for img in glob(path)]


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
        self.double_speed = False
        self.navigator = Navigator()

    def create_wall(self, x, y, n):
        for i in range(n):
            for j in range(n):
                tile = Tile(x + i * TILE_SIZE, y + j * TILE_SIZE)
                self.all_sprites.add(tile)
                self.tiles_list.add(tile)
                self.player.collide_list.add(tile)

    def add_enemy(self, enemy):
        self.all_sprites.add(enemy)
        self.enemy_list.add(enemy)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        self.platform_list = pg.sprite.Group()
        self.tiles_list = pg.sprite.Group()
        self.enemy_list = pg.sprite.Group()

        self.gold = pg.sprite.Group()

        money = create_gold(WIDTH / 2, HEIGHT / 2)
        self.gold.add(money)
        self.all_sprites.add(money)
        self.player = create_player(WIDTH / 3, HEIGHT / 2)
        self.all_sprites.add(self.player)

        for i in range(1, 5):
            self.add_enemy(create_enemy(EnemyType.WORM, WIDTH / 3, HEIGHT / 2, self.player))
            self.add_enemy(create_enemy(EnemyType.SLIME, WIDTH - 50, HEIGHT - 50, self.player))
            self.add_enemy(create_enemy(EnemyType.GHOST, WIDTH - 50, HEIGHT / 2, self.player))

        self.add_enemy(SlimeBlock(-500, HEIGHT / 2, 150, 150, None, self.player))

        self.right_wall = Platform(WIDTH * 4, 0, 120, HEIGHT)
        self.platform_list.add(self.right_wall)
        self.all_sprites.add(self.right_wall)
        self.player.collide_list.add(self.right_wall)

        p2 = Platform(WIDTH / 2 - 400, 100, 200, 20)
        p3 = Platform(WIDTH / 2 - 200, HEIGHT * 9 / 10, 100, 20)
        self.platform_list.add(p2)
        self.platform_list.add(p3)

        self.all_sprites.add(p2)
        self.all_sprites.add(p3)

        self.player.collide_list.add(p2)
        self.player.collide_list.add(p3)

        self.create_wall(room[0][8][0], room[0][8][1] + TILE_SIZE * 2, 2)

        for i in range(3):
            random = randint(3 * i, 3 * i + 2)
            n = randint(1, 4)
            self.create_wall(room[1][random][0], room[1][random][1], n)

        for i in range(3):
            random = randint(3 * i, 3 * i + 2)
            n = randint(1, 4)
            self.create_wall(room[2][random][0], room[2][random][1], n)

        for i in range(3):
            random = randint(3 * i, 3 * i + 2)
            n = randint(1, 4)
            self.create_wall(room[3][random][0], room[3][random][1], n)

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):

        for enemy in self.enemy_list:
            counter = 1000000
            if abs(
                    enemy.rect.x - self.player.rect.x) <= self.player.rect.width / 2 and self.player.rect.bottom == enemy.rect.bottom:
                if counter == 1000000:
                    self.player.hp -= 1
                counter -= 1
                if counter == 0:
                    counter = 1000000

            counter_ghost = 1000000
            if isinstance(enemy, Ghost) and abs(
                    enemy.rect.x - self.player.rect.x) <= self.player.rect.width / 2 and abs(
                enemy.rect.y - self.player.rect.y) <= self.player.rect.height / 2:
                if counter_ghost == 1000000:
                    self.player.hp -= 1
                counter_ghost -= 1
                if counter_ghost == 0:
                    counter_ghost = 1000000

        if self.player.hp <= 0:
            self.player.kill()
            self.playing = False

        for gold in self.gold:
            if abs(
                    gold.rect.x - self.player.rect.x) <= self.player.rect.width / 2 and self.player.rect.bottom == gold.rect.bottom:
                gold.kill()
                self.player.money += 100

        self.all_sprites.update()
        # print(self.player.vel_y)

    def events(self):
        have_jumped = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    if self.double_speed:
                        self.player.go_left_fast()
                    else:
                        self.player.go_left()
                if event.key == pg.K_RIGHT:
                    if self.double_speed:
                        self.player.go_right_fast()
                    else:
                        self.player.go_right()
                if event.key == pg.K_LSHIFT:
                    if not self.double_speed:
                        self.double_speed = True
                    else:
                        self.double_speed = False
                if event.key == pg.K_UP:
                    self.player.jump()
                    have_jumped = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and self.player.vel_x < 0:
                    self.player.stop()
                if event.key == pg.K_RIGHT and self.player.vel_x > 0:
                    self.player.stop()

        self.all_sprites.update()

        if self.player.rect.right >= 500:
            diff = self.player.rect.right - 500  # shift the world left
            self.player.rect.right = 500
            self.shift_world(-diff)

        if self.player.rect.left <= 500:
            diff = 500 - self.player.rect.left  # shift the world walk
            self.player.rect.left = 500
            self.shift_world(diff)

        if abs((self.right_wall.rect.x - self.right_wall.rect.width / 2) - (
                self.player.rect.x + self.player.rect.width / 2)) <= 25:
            self.navigator.go_to_store()

    def draw_stats_bar(self):
        stats = "HP: " + str(self.player.hp) + ", money: " + str(self.player.money)
        self.navigator.draw_text(stats, 20, WHITE, 80, 20)

        if self.player.got_double_speed:
            features = "You've got double speed!"
            self.navigator.draw_text(features, 20, WHITE, 120, 40)

    def draw(self):
        self.screen.fill(RED)
        self.draw_stats_bar()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def shift_world(self, shift_x):
        self.world_shift += shift_x

        for platform in self.platform_list:
            platform.rect.x += shift_x

        for tile in self.tiles_list:
            tile.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for gold in self.gold:
            gold.rect.x += shift_x


g = Game()
nav = Navigator()
nav.set_game(g)
nav.show_start_screen()
while g.running:
    g.new()
    nav.show_go_screen()

pg.quit()
