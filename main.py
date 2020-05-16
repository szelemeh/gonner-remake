import pygame as pg
import random

from settings import *
from sprites import *
from enemies import *


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
        self.font_name = pg.font.match_font(FONT_NAME)

    def create_wall(self, x, y, n):
        for i in range(n):
            for j in range(n):
                tile = Tile(x + i * TILE_SIZE, y + j * TILE_SIZE)
                self.all_sprites.add(tile)
                self.tiles_list.add(tile)
                self.player.collide_list.add(tile)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        self.all_objects = pg.sprite.Group()
        self.platform_list = pg.sprite.Group()
        self.tiles_list = pg.sprite.Group()
        self.enemy_list = pg.sprite.Group()


        self.player = Player()
        self.all_sprites.add(self.player)

        self.worm = Worm(WIDTH / 3, HEIGHT / 2, 63, 23, self.player)
        self.slime = Slime(WIDTH / 3, HEIGHT / 2, 63, 23, self.player)
        self.ghost = Ghost(WIDTH / 3, HEIGHT / 2, 63, 23, self.player)

        self.enemy_list.add(self.worm)
        self.enemy_list.add(self.ghost)
        self.enemy_list.add(self.slime)
        self.all_sprites.add(self.worm)
        self.all_sprites.add(self.slime)
        self.all_sprites.add(self.ghost)

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
            random = randint(3*i, 3*i + 2)
            n = randint(1, 4)
            self.create_wall(room[1][random][0], room[1][random][1], n)
        
        for i in range(3):
            random = randint(3*i, 3*i + 2)
            n = randint(1, 4)
            self.create_wall(room[2][random][0], room[2][random][1], n)

        for i in range(3):
            random = randint(3*i, 3*i + 2)
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
            if abs(enemy.rect.x - self.player.rect.x) == self.player.rect.width / 2 and self.player.rect.bottom == enemy.rect.bottom:
                self.player.kill()
                self.playing = False

        self.all_sprites.update()
        self.worm.update()

    def events(self):
        # Game Loop - events

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.go_left()
                if event.key == pg.K_RIGHT:
                    self.player.go_right()
                    go_right = True
                if event.key == pg.K_UP:
                    self.player.jump()

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pg.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()

        self.all_sprites.update()

        if self.player.rect.right >= 500:
            diff = self.player.rect.right - 500 # shift the world left
            self.player.rect.right = 500
            self.shift_world(-diff)

        if self.player.rect.left <= 500:
            diff = 500 - self.player.rect.left # shift the world right
            self.player.rect.left = 500
            self.shift_world(diff)


        if( abs( (self.right_wall.rect.x - self.right_wall.rect.width / 2) - (self.player.rect.x + self.player.rect.width / 2)) == self.player.rect.width):
            self.go_to_store()
            self.playing = False

    
    def draw(self):

        self.screen.fill(RED)

        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        print("Start")
        self.screen.fill(RED)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use arrows to move and jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        print("End")
        if not self.running:
            return
        self.screen.fill(RED)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        pg.display.flip()
        self.wait_for_key()

    def shift_world(self, shift_x):
        self.world_shift += shift_x

        for platform in self.platform_list:
            platform.rect.x += shift_x

        for tile in self.tiles_list:
            tile.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def go_to_store(self):
        print("is in store")
        self.show_go_screen()

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
