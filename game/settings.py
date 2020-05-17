TITLE = "GoNNER"
WIDTH = 1023
HEIGHT = 576
FPS = 60

FONT_NAME = 'arial'

TILE_SIZE = 32

# Player properties
PLAYER_SPEED = 6

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (122, 23, 46)
GREEN = (31, 122, 31)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (72, 132, 130)
GREY = (50, 32, 36)

area_h = HEIGHT / 3
area_w = WIDTH / 3

room = [[[0 for z in range(4)] for x in range(9)] for y in range(4)]

room[0] = [
    [0, 0, area_w, area_h],
    [area_w, 0, area_w * 2, area_h],
    [area_w * 2, 0, area_w * 3, area_h],

    [0, area_h, area_w, area_h * 2],
    [area_w, area_h, area_w * 2, area_h * 2],
    [area_w * 2, area_h, area_w * 3, area_h * 2],

    [0, area_h * 2, area_w, area_h * 3],
    [area_w, area_h * 2, area_w * 2, area_h * 3],
    [area_w * 2, area_h * 2, area_w * 3, area_h * 3],
]

room[1] = [
    [0 + WIDTH, 0, area_w + WIDTH, area_h],
    [area_w + WIDTH, 0, area_w * 2 + WIDTH, area_h],
    [area_w * 2 + WIDTH, 0, area_w * 3 + WIDTH, area_h],

    [0 + WIDTH, area_h, area_w + WIDTH, area_h * 2],
    [area_w + WIDTH, area_h, area_w * 2 + WIDTH, area_h * 2],
    [area_w * 2 + WIDTH, area_h, area_w * 3 + WIDTH, area_h * 2],

    [0 + WIDTH, area_h * 2, area_w + WIDTH, area_h * 3],
    [area_w + WIDTH, area_h * 2, area_w * 2 + WIDTH, area_h * 3],
    [area_w * 2 + WIDTH, area_h * 2, area_w * 3 + WIDTH, area_h * 3],
]

room[2] = [
    [0 + WIDTH * 2, 0, area_w + WIDTH * 2, area_h],
    [area_w + WIDTH * 2, 0, area_w * 2 + WIDTH * 2, area_h],
    [area_w * 2 + WIDTH * 2, 0, area_w * 3 + WIDTH * 2, area_h],

    [0 + WIDTH * 2, area_h, area_w + WIDTH * 2, area_h * 2],
    [area_w + WIDTH * 2, area_h, area_w * 2 + WIDTH * 2, area_h * 2],
    [area_w * 2 + WIDTH * 2, area_h, area_w * 3 + WIDTH * 2, area_h * 2],

    [0 + WIDTH * 2, area_h * 2, area_w + WIDTH * 2, area_h * 3],
    [area_w + WIDTH * 2, area_h * 2, area_w * 2 + WIDTH * 2, area_h * 3],
    [area_w * 2 + WIDTH * 2, area_h * 2, area_w * 3 + WIDTH * 2, area_h * 3],
]

room[3] = [
    [0 + WIDTH * 3, 0, area_w + WIDTH * 3, area_h],
    [area_w + WIDTH * 3, 0, area_w * 2 + WIDTH * 3, area_h],
    [area_w * 2 + WIDTH * 3, 0, area_w * 3 + WIDTH * 3, area_h],

    [0 + WIDTH * 3, area_h, area_w + WIDTH * 3, area_h * 2],
    [area_w + WIDTH * 3, area_h, area_w * 2 + WIDTH * 3, area_h * 2],
    [area_w * 2 + WIDTH * 3, area_h, area_w * 3 + WIDTH * 3, area_h * 2],

    [0 + WIDTH * 3, area_h * 2, area_w + WIDTH * 3, area_h * 3],
    [area_w + WIDTH * 3, area_h * 2, area_w * 2 + WIDTH * 3, area_h * 3],
    [area_w * 2 + WIDTH * 3, area_h * 2, area_w * 3 + WIDTH * 3, area_h * 3],
]

# Player properties
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.12

# Mob properties
MOB_ACCELERATION = 1
MOB_FRICTION = -0.2
