from random import randint

import pygame as pg

from creator import Creator
from game.camera import Camera
from game.navigation import Navigator
from game.settings import *
from sprites.enemies.air_enemies.ghost import Ghost
from sprites.enemies.enemy import EnemyType


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.can_jump = True
        self.double_speed = False

        self.navigator = Navigator()

    def add_enemy(self, enemy):
        self.all_sprites.add(enemy)
        self.enemy_list.add(enemy)

    def new(self):
        creator = Creator()
        creator.create_gold(WIDTH / 2, HEIGHT / 2)

        self.gold = pg.sprite.Group()

        self.player = creator.create_player(WIDTH / 3, HEIGHT / 2)

        for i in range(1, 5):
            creator.create_enemy(EnemyType.WORM, WIDTH / 3, HEIGHT / 2, self.player)
            creator.create_enemy(EnemyType.SLIME, WIDTH - 50, HEIGHT - 50, self.player)
            creator.create_enemy(EnemyType.GHOST, WIDTH - 50, HEIGHT / 2, self.player)

        creator.create_enemy(EnemyType.SLIME_BLOCK, -500, HEIGHT / 2, self.player)

        self.right_wall = creator.create_platform(WIDTH * 4, 0, 120, HEIGHT)

        creator.create_platform(WIDTH / 2 - 400, 100, 200, 20)
        creator.create_platform(WIDTH / 2 - 200, HEIGHT * 9 / 10, 100, 20)

        creator.create_wall(room[0][8][0], room[0][8][1] + TILE_SIZE * 2, 2)

        for i in range(3):
            random = randint(3 * i, 3 * i + 2)
            n = randint(1, 4)
            creator.create_wall(room[1][random][0], room[1][random][1], n)

        for i in range(3):
            random = randint(3 * i, 3 * i + 2)
            n = randint(1, 4)
            creator.create_wall(room[2][random][0], room[2][random][1], n)

        for i in range(3):
            random = randint(3 * i, 3 * i + 2)
            n = randint(1, 4)
            creator.create_wall(room[3][random][0], room[3][random][1], n)

        self.all_sprites = creator.all_sprites
        self.platform_list = creator.platforms
        self.tiles_list = creator.tiles
        self.enemy_list = creator.enemies
        self.player.collide_list = creator.player_collide_list
        self.camera = Camera(self.player, creator.shiftable)
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
        self.camera.update()
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


g = Game()
nav = Navigator()
nav.set_game(g)
nav.show_start_screen()
while g.running:
    g.new()
    nav.show_go_screen()

pg.quit()
