

class Camera:
    def __init__(self, player, sprites_to_shift):
        self.sprites_to_shift = sprites_to_shift
        self.player = player
        self.world_shift = 0

    def add_player(self, player):
        self.player = player

    def __shift_world(self, shift_x):
        self.world_shift += shift_x

        for o in self.sprites_to_shift:
            o.rect.x += shift_x

        # for platform in self.platform_list:
        #     platform.rect.x += shift_x
        #
        # for tile in self.tiles_list:
        #     tile.rect.x += shift_x
        #
        # for enemy in self.enemy_list:
        #     enemy.rect.x += shift_x
        #
        # for gold in self.gold:
        #     gold.rect.x += shift_x

    def update(self):
        if self.player.rect.right >= 500:
            diff = self.player.rect.right - 500  # shift the world left
            self.player.rect.right = 500
            self.__shift_world(-diff)

        if self.player.rect.left <= 500:
            diff = 500 - self.player.rect.left  # shift the world walk
            self.player.rect.left = 500
            self.__shift_world(diff)
