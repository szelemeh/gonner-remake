class Camera:
    def __init__(self, player, sprites_to_shift, texts):
        self.sprites_to_shift = sprites_to_shift
        self.texts = texts
        self.player = player
        self.world_shift = 0

    def add_player(self, player):
        self.player = player

    def __shift_world(self, shift_x):
        self.world_shift += shift_x

        for o in self.sprites_to_shift:
            o.rect.x += shift_x

        for _, rect in self.texts:
            rect.midtop = (rect.midtop[0] + shift_x, rect.midtop[1])

    def update(self):
        if self.player.rect.right >= 500:
            diff = self.player.rect.right - 500  # shift the world left
            self.player.rect.right = 500
            self.__shift_world(-diff)

        if self.player.rect.left <= 500:
            diff = 500 - self.player.rect.left  # shift the world walk
            self.player.rect.left = 500
            self.__shift_world(diff)
