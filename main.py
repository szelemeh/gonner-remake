
import pygame
from sprites import *
from settings import *



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

    def create_wall(self, x, y, n):
        for i in range(n):
            for j in range(n):
                tile = Tile(x + i * TILE_SIZE, y + j * TILE_SIZE)
                self.all_sprites.add(tile)
                self.tiles_list.add(tile)
                self.player.collide_list.add(tile)


    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        self.all_objects = pg.sprite.Group()
        self.platform_list = pg.sprite.Group()
        self.tiles_list = pg.sprite.Group()
        self.enemy_list = pg.sprite.Group()

        # self.create_wall(WIDTH / 2, HEIGHT / 2, 2)

        self.player = Player()
        self.all_sprites.add(self.player)
        self.enemy = Mob()
        self.enemy_list.add(self.enemy)
        self.all_sprites.add(self.enemy)
        self.player.collide_list.add(self.enemy)


        #ceiling = Platform(0, 0, WIDTH * 10, 100)
        #self.platform_list.add(ceiling)

        p2 = Platform(WIDTH / 2 - 400, 100, 200, 20)
        p3 = Platform(WIDTH / 2 - 200, HEIGHT * 9 / 10, 100, 20)
        self.platform_list.add(p2)
        self.platform_list.add(p3)
        
        self.all_sprites.add(p2)
        self.all_sprites.add(p3)
        #self.all_sprites.add(ceiling)

        self.player.collide_list.add(p2)
        self.player.collide_list.add(p3)
        #self.player.collide_list.add(ceiling)

        self.run()


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        #self.player.update()
        #self.all_objects.update()

    def events(self):
        # Game Loop - events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.go_left()
                if event.key == pg.K_RIGHT:
                    self.player.go_right()
                if event.key == pg.K_UP:
                    self.player.jump()

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pg.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()


        self.all_sprites.update()

        if self.player.rect.right >= 500:
            diff = self.player.rect.right - 500
            self.player.rect.right = 500
            self.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if self.player.rect.left <= 120:
            diff = 120 - self.player.rect.left
            self.player.rect.left = 120
            self.shift_world(diff)
        


    def draw(self):
 
        # Draw the background
        self.screen.fill(RED)
 
        # Draw all the sprite lists that we have
        #self.player_sprite.draw(self.screen)
        #self.all_objects.draw(self.screen)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        pass # here there will be game start screen

    def show_go_screen(self):
        pass # here there will be end game screen
 
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for tile in self.tiles_list:
            tile.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x


# class Level():
#     """ This is a generic super-class used to define a level.
#         Create a child class for each level with level-specific
#         info. """
 
#     def __init__(self, player):
#         """ Constructor. Pass in a handle to player. Needed for when moving
#             platforms collide with the player. """
#         self.platform_list = pygame.sprite.Group()
#         self.enemy_list = pygame.sprite.Group()
#         self.player = player
 
#         # How far this world has been scrolled left/right
#         self.world_shift = 0
 
#     # Update everythign on this level
#     def update(self):
#         """ Update everything in this level."""
#         self.platform_list.update()
#         self.enemy_list.update()
 
#     def draw(self, screen):
#         """ Draw everything on this level. """
 
#         # Draw the background
#         screen.fill(RED)
 
#         # Draw all the sprite lists that we have
#         self.platform_list.draw(screen)
#         self.enemy_list.draw(screen)
 
#     def shift_world(self, shift_x):
#         """ When the user moves left/right and we need to scroll
#         everything: """
 
#         # Keep track of the shift amount
#         self.world_shift += shift_x
 
#         # Go through all the sprite lists and shift
#         for platform in self.platform_list:
#             platform.rect.x += shift_x
 
#         for enemy in self.enemy_list:
#             enemy.rect.x += shift_x
 
 
# Create platforms for the level
# class Level_01(Level):
#     """ Definition for level 1. """
 
#     def __init__(self, player):
#         """ Create level 1. """
 
#         # Call the parent constructor
#         Level.__init__(self, player)
 
#         self.level_limit = -1000
#         #self.level_limit = -WIDTH

#         ceiling = Platform(0, 0, WIDTH * 10, 100)
#         self.platform_list.add(ceiling)

#         p2 = Platform(WIDTH / 2 - 400, 100, 200, 20)
#         p3 = Platform(WIDTH / 2 - 200, HEIGHT * 9 / 10, 100, 20)
#         self.platform_list.add(p2)
#         self.platform_list.add(p3)
 
 
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
 
# def main():
#     """ Main Program """
#     #pygame.init()
 
#     # Set the height and width of the screen
#     #size = [WIDTH, HEIGHT]
#     #screen = pygame.display.set_mode(size)
 
#     # Create the player
#     #player = Player()
 
#     # Create all the levels
#     #level_list = []
#     #level_list.append(Level_01(player))
 
#     # Set the current level
#     #current_level_no = 0
#     #current_level = level_list[current_level_no]
 
#     active_sprite_list = pygame.sprite.Group()
#     player.level = current_level
 
#     player.rect.x = 340
#     player.rect.y = HEIGHT - player.rect.height
#     active_sprite_list.add(player)
 
#     # Loop until the user clicks the close button.
#     done = False
 
#     # Used to manage how fast the screen updates
#     clock = pygame.time.Clock()
 
#     # -------- Main Program Loop -----------
#     while not done:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 done = True
 
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_LEFT:
#                     player.go_left()
#                 if event.key == pygame.K_RIGHT:
#                     player.go_right()
#                 if event.key == pygame.K_UP:
#                     player.jump()
 
#             if event.type == pygame.KEYUP:
#                 if event.key == pygame.K_LEFT and player.change_x < 0:
#                     player.stop()
#                 if event.key == pygame.K_RIGHT and player.change_x > 0:
#                     player.stop()
 
#         active_sprite_list.update() # Update the player.
#         current_level.update() # Update items in the level
 
#         # If the player gets near the right side, shift the world left (-x)
#         if player.rect.right >= 500:
#             diff = player.rect.right - 500
#             player.rect.right = 500
#             current_level.shift_world(-diff)
 
#         # If the player gets near the left side, shift the world right (+x)
#         if player.rect.left <= 120:
#             diff = 120 - player.rect.left
#             player.rect.left = 120
#             current_level.shift_world(diff)
        
#         # If the player gets to the end of the level, go to the next level
#         #current_position = player.rect.x + current_level.world_shift
#         #if current_position < current_level.level_limit:
#         #    player.rect.x = 120
#             # if current_level_no < len(level_list)-1:
#             #     current_level_no += 1
#             #     current_level = level_list[current_level_no]
#             #     player.level = current_level

#         current_level.draw(screen)
#         active_sprite_list.draw(screen)
#         clock.tick(60)
#         pygame.display.flip()

#     pygame.quit()
 
# if __name__ == "__main__":
#     main()
