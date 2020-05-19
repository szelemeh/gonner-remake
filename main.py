from random import randint

import pygame as pg

from creator import Creator
from game.camera import Camera
from game.navigation import Navigator
from game.settings import *
from sprites.enemies.air_enemies.air_enemy import AirEnemy
from sprites.enemies.enemy import EnemyType
from sprites.weapon.weapon import Weapon


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

    def new(self):
        self.creator = Creator()
        self.creator.create_gold(WIDTH / 2, HEIGHT / 2)

        self.gold = pg.sprite.Group()

        self.player = self.creator.create_player(WIDTH / 3, HEIGHT / 2)
        self.player.weapon = Weapon(self.creator)

        for i in range(1, 5):
            self.creator.create_enemy(EnemyType.WORM, WIDTH / 3, HEIGHT / 2, self.player)
            self.creator.create_enemy(EnemyType.SLIME, WIDTH - 50, HEIGHT - 50, self.player)
            self.creator.create_enemy(EnemyType.GHOST, WIDTH - 50, HEIGHT / 2, self.player)

        # self.creator.create_enemy(EnemyType.SLIME_BLOCK, -500, HEIGHT / 2, self.player)

        self.right_wall = self.creator.create_platform(WIDTH * 4, 0, 120, HEIGHT)

        self.creator.create_platform(WIDTH / 2 - 400, 100, 200, 20)
        self.creator.create_platform(WIDTH / 2 - 200, HEIGHT * 9 / 10, 100, 20)

        self.creator.create_wall(room[0][8][0], room[0][8][1] + TILE_SIZE * 2, 2)

        for i in range(3):
            random = randint(3 * i, 3 * i + 2)
            n = randint(1, 4)
            self.creator.create_wall(room[1][random][0], room[1][random][1], n)

        for i in range(3):
            random = randint(3 * i, 3 * i + 2)
            n = randint(1, 4)
            self.creator.create_wall(room[2][random][0], room[2][random][1], n)

        for i in range(3):
            random = randint(3 * i, 3 * i + 2)
            n = randint(1, 4)
            self.creator.create_wall(room[3][random][0], room[3][random][1], n)

        self.all_sprites = self.creator.all_sprites
        self.platform_list = self.creator.platforms
        self.tile_list = self.creator.tiles
        self.enemy_list = self.creator.enemies
        self.coin_list = self.creator.coins
        self.player.collide_list = self.creator.player_collide_list
        self.camera = Camera(self.player, self.creator.shiftable)
        self.bullet_list = self.creator.bullets
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):

        if self.player.hp <= 0:
            self.player.kill()
            self.playing = False

        for coin in pg.sprite.spritecollide(self.player, self.coin_list, False):
            coin.kill()
            self.player.money += 100

        for enemy in pg.sprite.spritecollide(self.player, self.enemy_list, False):
            if abs(enemy.rect.x - self.player.rect.x) <= self.player.rect.width / 2 \
                    and self.player.rect.bottom == enemy.rect.bottom:
                self.player.receive_damage(1)

            if isinstance(enemy, AirEnemy) \
                    and abs(enemy.rect.x - self.player.rect.x) <= self.player.rect.width / 2 \
                    and abs(enemy.rect.y - self.player.rect.y) <= self.player.rect.height / 2:
                self.player.receive_damage(1)

        pg.sprite.groupcollide(self.bullet_list, self.platform_list, True, False)
        pg.sprite.groupcollide(self.bullet_list, self.tile_list, True, False)
        pg.sprite.groupcollide(self.bullet_list, self.enemy_list, True, True)

        self.all_sprites.update()
        self.camera.update()

    def events(self):
        have_jumped = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.fire()

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
