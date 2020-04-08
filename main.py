import pygame as pg
import random
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.can_jump = False


    def create_wall(self, x, y, n):
        for i in range(n):
            for j in range(n):
                tile = Tile(x + i * TILE_SIZE, y + j * TILE_SIZE)
                self.all_sprites.add(tile)
                self.tiles.add(tile)


    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.create_wall(WIDTH / 2, HEIGHT / 2, 2)

        self.player = Player()
        self.all_sprites.add(self.player)

        ground = Platform(0, HEIGHT - 32, WIDTH, 32)
        self.all_sprites.add(ground)
        self.platforms.add(ground)
        p2 = Platform(WIDTH / 2 - 400, HEIGHT * 3 / 4, 200, 20)
        self.all_sprites.add(p2)
        self.platforms.add(p2)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        hits_platform = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits_platform:
            if self.player.rect.top > hits_platform[0].rect.bottom - hits_platform[0].height / 2:
                self.player.velocity.y = 0
            else:
                self.player.position.y = hits_platform[0].rect.top
                self.player.velocity.y = 0
                self.can_jump = True

        hits_tile = pg.sprite.spritecollide(self.player, self.tiles, False)
        if hits_tile:
            if self.player.rect.top > hits_tile[0].rect.bottom - hits_tile[0].size / 2:
                self.player.velocity.y = 0
            else:
                self.player.position.y = hits_tile[0].rect.top
                self.player.velocity.y = 0
                self.can_jump = True

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False


            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    if(self.can_jump):
                        self.player.jump()
                        self.can_jump = False


    def draw(self):
        # Game Loop - draw
        self.screen.fill(RED)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
