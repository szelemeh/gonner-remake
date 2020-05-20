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

        self.creator = Creator()
        self.creator.create_gold(WIDTH / 2, HEIGHT / 2)

        self.player = self.creator.create_player(WIDTH / 3, HEIGHT / 2)
        self.player.weapon = Weapon(self.creator)

        self.all_sprites = self.creator.all_sprites
        self.platform_list = self.creator.platforms
        self.tile_list = self.creator.tiles
        self.enemy_list = self.creator.enemies
        self.coin_list = self.creator.coins
        self.player.collide_list = self.creator.player_collide_list
        self.camera = Camera(self.player, self.creator.shiftable)
        self.bullet_list = self.creator.bullets


    def build_level_01(self):

        for i in range(1, 5):
            self.creator.create_enemy(EnemyType.WORM, WIDTH / 3, HEIGHT / 2, self.player)
            self.creator.create_enemy(EnemyType.SLIME, WIDTH - 50, HEIGHT - 50, self.player)
            self.creator.create_enemy(EnemyType.GHOST, WIDTH - 50, HEIGHT / 2, self.player)

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



    def build_level_02(self):

        self.creator.empty_all_objects()
        self.all_sprites.add(self.player)

        self.right_wall = self.creator.create_platform(WIDTH * 4, 0, 120, HEIGHT)
        self.map = []
        with open('map_2.txt', 'r') as f:
            for line in f:
                self.map.append(line)

        for row, tiles in enumerate(self.map):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    self.creator.create_wall(col * TILE_SIZE, row * TILE_SIZE, 1)
                    print("created tile")

    def build_level_03(self):

        self.creator.empty_all_objects()
        self.all_sprites.add(self.player)

        self.right_wall = self.creator.create_platform(WIDTH * 4, 0, 120, HEIGHT)

        self.creator.create_enemy(EnemyType.SLIME_BLOCK, WIDTH / 2, HEIGHT / 2, self.player)


    def new(self, number):
        if(number == 0):
            self.build_level_01()
            self.run(number)
        elif(number == 1):
            self.build_level_02()
            self.run(number)
        elif(number == 2):
            self.build_level_03()
            self.run(number)
        else:
            return

    def run(self, number):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events(number)
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

        collision_dict = pg.sprite.groupcollide(self.bullet_list, self.enemy_list, True, False)
        for bullet in collision_dict:
            for enemy in collision_dict[bullet]:
                enemy.hp -= bullet.damage


        self.all_sprites.update()
        self.camera.update()

    def events(self, number):
        have_jumped = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                self.navigator.show_go_screen()
                pg.quit()

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
                if(number == 0 or number == 1):
                    self.navigator.go_to_store()
                else:
                    self.navigator.show_go_screen()

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



Levels = 3
g = Game()
nav = Navigator()
nav.set_game(g)
nav.show_start_screen()
while g.running:
    for lvl in range(Levels):
        print("You're on ", lvl)
        g.new(lvl)
    g.running = False
nav.show_go_screen()
pg.quit()
