# code from https://stackoverflow.com/questions/45909318/show-pymunk-with-pygame-python


import math

import pygame as pg
import pymunk as pm
from pymunk import Vec2d


def flipy(p):
    """Convert chipmunk coordinates to pygame coordinates."""
    return Vec2d(p[0], -p[1]+600)


class Entity(pg.sprite.Sprite):

    def __init__(self, pos, space):
        super().__init__()
        self.image = pg.Surface((46, 52), pg.SRCALPHA)
        pg.draw.polygon(self.image, (0, 50, 200),
                        [(0, 0), (48, 0), (48, 54), (24, 54)])
        self.orig_image = self.image
        self.rect = self.image.get_rect(topleft=pos)
        vs = [(-23, 26), (23, 26), (23, -26), (0, -26)]
        mass = 1
        moment = pm.moment_for_poly(mass, vs)
        self.body = pm.Body(mass, moment)
        self.shape = pm.Poly(self.body, vs)
        self.shape.friction = .9
        self.body.position = pos
        self.space = space
        self.space.add(self.body, self.shape)

    def update(self, dt):
        pos = flipy(self.body.position)
        self.rect.center = pos
        self.image = pg.transform.rotate(
            self.orig_image, math.degrees(self.body.angle))
        self.rect = self.image.get_rect(center=self.rect.center)
        # Remove sprites that have left the screen.
        if pos.x < 20 or pos.y > 560:
            self.space.remove(self.body, self.shape)
            self.kill()

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a:
                self.body.angular_velocity = 5.5
            elif event.key == pg.K_w:
                self.body.apply_impulse_at_local_point(Vec2d(0, 900))


class Game:

    def __init__(self):
        self.done = False
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((800, 600))
        self.gray = pg.Color('gray68')
        self.red = pg.Color('red')

        # Pymunk stuff.
        self.space = pm.Space()
        self.space.gravity = Vec2d(0.0, -900.0)
        self.static_lines = [
            pm.Segment(self.space.static_body, (60, 100), (370, 100), 0),
            #pm.Segment(self.space.static_body, (370, 100), (600, 300), 0),
            ]
        for lin in self.static_lines:
            lin.friction = 0.8
        self.space.add(self.static_lines)
        # A sprite group which holds the pygame.sprite.Sprite objects.
        self.sprite_group = pg.sprite.Group(Entity((150, 200), self.space))

    def run(self):
        while not self.done:
            self.dt = self.clock.tick(30) / 1000
            self.handle_events()
            self.run_logic()
            self.draw()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                self.sprite_group.add(Entity(flipy(event.pos), self.space))
            for sprite in self.sprite_group:
                sprite.handle_event(event)

    def run_logic(self):
        self.space.step(1/60)  # Update physics.
        self.sprite_group.update(self.dt)  # Update pygame sprites.

    def draw(self):
        self.screen.fill(pg.Color(140, 120, 110))
        for line in self.static_lines:
            body = line.body
            p1 = flipy(body.position + line.a.rotated(body.angle))
            p2 = flipy(body.position + line.b.rotated(body.angle))
            pg.draw.line(self.screen, self.gray, p1, p2, 5)
        self.sprite_group.draw(self.screen)
        # Debug draw. Outlines of the Pymunk shapes.
        for obj in self.sprite_group:
            shape = obj.shape
            ps = [pos.rotated(shape.body.angle) + shape.body.position
                  for pos in shape.get_vertices()]
            ps = [flipy((pos)) for pos in ps]
            ps += [ps[0]]
            pg.draw.lines(self.screen, self.red, False, ps, 1)

        pg.display.flip()


if __name__ == '__main__':
    pg.init()
    Game().run()
    pg.quit()