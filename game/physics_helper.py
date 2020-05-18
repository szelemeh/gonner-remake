from numpy import sign
from math import sqrt


def get_next_step_to(point_from, point_to, velocity):
    # from x, y
    fx = point_from[0]
    fy = point_from[1]
    # to x, y
    tx = point_to[0]
    ty = point_to[1]
    # a, b, c - sides of right triangle
    c = get_distance_between(tx, ty, fx, fy)
    a = abs(fy - ty)
    b = abs(fx - tx)
    # sin and cos of angle adjacent to b
    sin = a / c
    cos = b / c
    # splitting velocity on two dimensions
    return (sign(tx - fx) * velocity * cos,
            sign(ty - fy) * velocity * sin)


def get_distance_between(x1, y1, x2, y2):
    distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance
