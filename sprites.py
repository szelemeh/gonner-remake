# Sprite classes for the game

from settings import *
import math
import pygame as pg
import pymunk as pm
from pymunk import Vec2d


def to_pg(p):
    """Convert chipmunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1] + HEIGHT)


def to_pm(p):
    """Convert pygame coordinates to chipmunk coordinates."""
    return Vec2d(p[0], p[1] - HEIGHT)


class Player(pg.sprite.Sprite):
    def __init__(self, game, space):
        super().__init__()
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()

        mass = 1
        vertices = [(-15, -20), (-15, 20), (15, 20), (15, -20)]
        moment = pm.moment_for_poly(mass, vertices)
        self.body = pm.Body(mass, moment)
        self.shape = pm.Poly(self.body, vertices)
        self.shape.friction = .9
        self.body.position = WIDTH / 2, HEIGHT / 2
        self.space = space
        self.space.add(self.body, self.shape)

    def update(self):
        grounding = {
            'normal': Vec2d.zero(),
            'penetration': Vec2d.zero(),
            'impulse': Vec2d.zero(),
            'position': Vec2d.zero(),
            'body': None
        }

        def f(arbiter):
            n = -arbiter.contact_point_set.normal
            if n.y > grounding['normal'].y:
                grounding['normal'] = n
                grounding['penetration'] = -arbiter.contact_point_set.points[0].distance
                grounding['body'] = arbiter.shapes[1].body
                grounding['impulse'] = arbiter.total_impulse
                grounding['position'] = arbiter.contact_point_set.points[0].point_b

        self.body.each_arbiter(f)

        well_grounded = False
        if grounding['body'] is not None \
                and abs(grounding['normal'].x / grounding['normal'].y) \
                < self.shape.friction:
            well_grounded = True

        ground_velocity = Vec2d.zero()
        if well_grounded:
            ground_velocity = grounding['body'].velocity

        keys = pg.key.get_pressed()

        if keys[pg.K_UP]:
            if well_grounded:
                jump_v = math.sqrt(2.0 * JUMP_HEIGHT * abs(self.space.gravity.y))
                impulse = (0, self.body.mass * (ground_velocity.y + jump_v))
                self.body.apply_impulse_at_local_point(impulse)

        target_vx = 0

        if self.body.velocity.x > .01:
            direction = 1
        elif self.body.velocity.x < -.01:
            direction = -1

        if keys[pg.K_LEFT]:
            direction = -1
            target_vx -= PLAYER_VELOCITY
        elif keys[pg.K_RIGHT]:
            direction = 1
            target_vx += PLAYER_VELOCITY

        self.shape.surface_velocity = (-target_vx, 0)

        position = to_pg(self.body.position)
        self.rect.midbottom = position


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, space):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y+h/2)

        self.space = space
        self.line = pm.Segment(self.space.static_body, to_pm((x, y)), to_pm((x+w, y)), h)
        self.line.friction = 0.8
        self.space.add(self.line)
