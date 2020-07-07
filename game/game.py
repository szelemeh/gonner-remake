import sys

import pygame as pg

from game.creator import Creator
from game.drawer import Drawer
from game.camera import Camera
from game.navigation import Navigator
from game.settings import *
from sprites.enemies.air_enemies.air_enemy import AirEnemy
from sprites.enemies.ground_enemies.slime_block import SlimeBlock
from sprites.weapon.weapon import Weapon


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.double_speed = False
        self.number_of_levels = 4

        self.navigator = Navigator(self)
        self.drawer = Drawer(self.screen)
        self.creator = Creator()

        self.init_player()
        self.init_sprite_lists()

        self.camera = Camera(self.player, self.creator.shiftable,
                             self.creator.texts)

        self.is_tutorial = False
        self.current_level = 0

    def init_sprite_lists(self):
        self.all_sprites = self.creator.all_sprites
        self.platform_list = self.creator.platforms
        self.tile_list = self.creator.tiles
        self.enemy_list = self.creator.enemies
        self.coin_list = self.creator.coins
        self.player.collide_list = self.creator.player_collide_list
        self.bullet_list = self.creator.bullets

    def init_player(self):
        self.player = self.creator.player
        self.player.weapon = Weapon(self.creator)

    def stop(self):
        self.playing = False
        self.running = False

    def new(self, level):
        """ Calls level or final level building and playing loop """
        self.current_level = level
        if level == self.number_of_levels - 1:
            self.creator.build_level_final(self.player)
            self.run()
        elif 0 <= level < self.number_of_levels - 1:
            self.creator.build_level(self.player)
            self.run()
        else:
            return

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            if self.playing:
                self.draw()

    def update(self):
        """ Handles screen updates """

        if self.player.hp <= 0:
            self.player.kill()
            self.navigator.show_go_screen()

        for coin in pg.sprite.spritecollide(self.player, self.coin_list,
                                            False):
            coin.kill()
            self.player.money += 30

        for enemy in pg.sprite.spritecollide(self.player, self.enemy_list,
                                             False):
            if abs(enemy.rect.x - self.player.rect.x) <= self.player.rect.width / 2 \
                    and self.player.rect.bottom == enemy.rect.bottom:
                self.player.receive_damage(1)

            if isinstance(enemy, AirEnemy) \
                    and abs(enemy.rect.x - self.player.rect.x) <= self.player.rect.width / 2 \
                    and abs(enemy.rect.y - self.player.rect.y) <= self.player.rect.height / 2:
                if not self.is_tutorial:
                    self.player.receive_damage(1)

            if isinstance(enemy, SlimeBlock) \
                    and abs(enemy.rect.x - self.player.rect.x) <= self.player.rect.width / 2 \
                    and abs(enemy.rect.y - self.player.rect.y) <= self.player.rect.height / 2:
                if not self.is_tutorial:
                    self.player.receive_damage(1)

        pg.sprite.groupcollide(self.bullet_list, self.platform_list, True,
                               False)
        pg.sprite.groupcollide(self.bullet_list, self.tile_list, True, False)

        collision_dict = pg.sprite.groupcollide(self.bullet_list,
                                                self.enemy_list, True, False)
        for bullet in collision_dict:
            for enemy in collision_dict[bullet]:
                enemy.hp -= bullet.damage

        self.all_sprites.update()
        self.camera.update()

    def events(self):
        """ Handles key events """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

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

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and self.player.vel_x < 0:
                    self.player.stop()
                if event.key == pg.K_RIGHT and self.player.vel_x > 0:
                    self.player.stop()

        self.all_sprites.update()


        if abs((self.creator.right_wall.rect.x -
                self.creator.right_wall.rect.width / 2) -
               (self.player.rect.x + self.player.rect.width / 2)) <= 25:
            if self.is_tutorial:
                self.navigator.show_tutorial_done_screen()
            else:
                if self.current_level < self.number_of_levels - 1:
                    self.navigator.go_to_store()
                elif self.is_boss_level():
                    if not self.creator.boss.alive():
                        self.navigator.show_congrats_screen()

    def draw_stats_bar(self):
        self.drawer.draw_player_stats(self.player)

        if self.is_boss_level():
            self.drawer.draw_health_bar(
                self.creator.boss, 700, 20, 5)

    def draw(self):
        self.screen.fill(RED)
        self.draw_stats_bar()
        self.all_sprites.draw(self.screen)
        if self.is_tutorial:
            self.blit_texts()
        pg.display.flip()

    def blit_texts(self):
        for sf, rect in self.creator.texts:
            self.screen.blit(sf, rect.midtop)

    def reset(self):
        self.player.hp = 15
        self.player.money = 0
        self.running = True
        self.playing = True
        pass

    def tutorial(self):
        self.is_tutorial = True
        self.creator.build_tutorial_level(self.player, self.screen)
        self.run()

    def is_boss_level(self):
        if self.is_tutorial:
            return False
        return self.current_level == self.number_of_levels - 1
